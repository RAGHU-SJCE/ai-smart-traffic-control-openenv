import asyncio
import os
import textwrap
from typing import List

from openai import OpenAI
from models import TrafficAction, SmartTrafficEnv


API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

TASK_NAME = "smart-traffic-control"
BENCHMARK = "openenv-v1"

MAX_STEPS = 20
TEMPERATURE = 0.3
MAX_TOKENS = 120
SUCCESS_SCORE_THRESHOLD = 0.5

MAX_TOTAL_REWARD = MAX_STEPS * 1.0


SYSTEM_PROMPT = textwrap.dedent("""
You are an expert traffic controller.

STRICT RULE:
Respond ONLY in format:
NS <number>
or
EW <number>

GOAL:
- Minimize wait time
- Balance traffic
- Avoid starvation
""").strip()


# =========================
# LOGGING
# =========================
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}", flush=True)


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


# =========================
# MODEL CALL
# =========================
def get_model_action(client):
    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Decide next traffic action"},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        return res.choices[0].message.content.strip()
    except:
        return "NS 20"


# =========================
# PARSE ACTION
# =========================
def parse_action(text):
    try:
        parts = text.strip().upper().split()
        if len(parts) != 2:
            raise ValueError()

        direction, duration = parts

        if direction not in ["NS", "EW"]:
            raise ValueError()

        duration = int(duration)
        duration = max(5, min(duration, 60))

        return TrafficAction(direction=direction, duration=duration)

    except:
        return TrafficAction(direction="NS", duration=20)


# =========================
# MAIN LOOP (🔥 FIXED HERE)
# =========================
async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = SmartTrafficEnv()

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

    try:
        result = await env.reset()

        for step in range(1, MAX_STEPS + 1):

            # ✅ FIX: dictionary access
            if result["done"]:
                break

            obs = result["observation"]

            action_text = get_model_action(client)
            action = parse_action(action_text)

            # =========================
            # SMART LOGIC
            # =========================
            ns_queue = obs.north_queue + obs.south_queue
            ew_queue = obs.east_queue + obs.west_queue

            ns_wait = obs.north_wait + obs.south_wait
            ew_wait = obs.east_wait + obs.west_wait

            ns_score = ns_queue * 1.2 + (ns_wait * 0.8)
            ew_score = ew_queue * 1.2 + (ew_wait * 0.8)

            if ns_score > ew_score:
                action.direction = "NS"
            else:
                action.direction = "EW"

            max_score = max(ns_score, ew_score)

            if max_score > 60:
                action.duration = 50
            elif max_score > 40:
                action.duration = 40
            elif max_score > 25:
                action.duration = 30
            elif max_score > 15:
                action.duration = 25
            else:
                action.duration = 15

            result = await env.step(action)

            # ✅ FIX: dictionary access
            reward = result["reward"] or 0.0
            done = result["done"]

            rewards.append(reward)
            steps_taken = step

            log_step(step, f"{action.direction} {action.duration}", reward, done, None)

            if done:
                break

        raw_score = sum(rewards) / MAX_TOTAL_REWARD
        score = max(0.0, min(raw_score, 1.0))
        success = score >= SUCCESS_SCORE_THRESHOLD

    finally:
        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    asyncio.run(main())