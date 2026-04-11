import os
from openai import OpenAI
from models import SmartTrafficEnv, TrafficAction

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

env = SmartTrafficEnv()

print("[START]")

for task in ["easy", "medium", "hard"]:

    print(f"[STEP] task={task}")

    state = env.reset(task)
    total_reward = 0

    for step in range(20):

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": str(state)}],
                max_tokens=5
            )

            txt = response.choices[0].message.content

            if "0" in txt:
                action_value = 0
            elif "1" in txt:
                action_value = 1
            else:
                raise ValueError()

        except:
            ns = state.north_queue + state.south_queue
            ew = state.east_queue + state.west_queue
            action_value = 0 if ns >= ew else 1

        result = env.step(TrafficAction(signal_phase=action_value))

        reward = result["reward"]
        total_reward += reward

        print(f"[STEP] step={step} action={action_value} reward={reward:.3f}")

        if result["done"]:
            break

        state = env.get_state()

    print(f"[STEP] task={task} total_reward={total_reward:.3f}")

print("[END]")