import gradio as gr
import asyncio
import matplotlib.pyplot as plt
import time

from models import SmartTrafficEnv, TrafficAction

# =========================
# GLOBALS
# =========================
env = SmartTrafficEnv("medium")
current_result = None
step_count = 0

history_ns = []
history_ew = []
rewards_history = []

running = False


# =========================
# VISUALS
# =========================
def moving_cars(n, offset):
    cars = ["🚗"] * min(n, 10)
    shifted = [" "] * offset + cars
    return "".join(shifted[:15])


def draw(obs, direction, frame):
    offset = frame % 5

    return f"""
    <div style="text-align:center;font-family:monospace;">
        <div>{moving_cars(obs.north_queue, offset)} 🚗</div>
        <div>{"🟢" if direction=="NS" else "🔴"}</div>

        <div style="display:flex;justify-content:center;">
            <div>{moving_cars(obs.west_queue, offset)} {"🟢" if direction=="EW" else "🔴"}</div>
            <div style="margin:0 20px;">+</div>
            <div>{"🟢" if direction=="EW" else "🔴"} {moving_cars(obs.east_queue, offset)}</div>
        </div>

        <div>{"🟢" if direction=="NS" else "🔴"}</div>
        <div>🚗 {moving_cars(obs.south_queue, offset)}</div>
    </div>
    """


# =========================
# AI LOGIC
# =========================
def ai_decision(obs):
    ns = obs.north_queue + obs.south_queue
    ew = obs.east_queue + obs.west_queue

    direction = "NS" if ns > ew else "EW"
    load = max(ns, ew)

    if load > 30:
        duration = 50
    elif load > 20:
        duration = 35
    elif load > 10:
        duration = 25
    else:
        duration = 15

    return direction, duration


# =========================
# GRAPH
# =========================
def plot_graph():
    fig, ax = plt.subplots()
    ax.plot(history_ns, label="NS")
    ax.plot(history_ew, label="EW")
    ax.set_title("Traffic Flow")
    ax.legend()
    return fig


# =========================
# RESET WITH DIFFICULTY
# =========================
def reset_env(difficulty):
    global env, current_result, step_count
    global history_ns, history_ew, rewards_history, running

    env = SmartTrafficEnv(difficulty)
    current_result = asyncio.run(env.reset())

    step_count = 0
    history_ns = []
    history_ew = []
    rewards_history = []
    running = False

    return update_ui(current_result, "NS")


# =========================
# MANUAL STEP
# =========================
def step_env(direction, duration):
    global current_result, step_count

    action = TrafficAction(direction=direction, duration=int(duration))
    current_result = asyncio.run(env.step(action))
    step_count += 1

    obs = current_result.observation

    history_ns.append(obs.north_queue + obs.south_queue)
    history_ew.append(obs.east_queue + obs.west_queue)
    rewards_history.append(current_result.reward)

    return update_ui(current_result, direction)


# =========================
# AUTO PLAY
# =========================
def auto_play(speed):
    global running, current_result, step_count

    running = True

    while running and step_count < 20:
        obs = current_result.observation

        direction, duration = ai_decision(obs)

        action = TrafficAction(direction=direction, duration=duration)
        current_result = asyncio.run(env.step(action))
        step_count += 1

        obs = current_result.observation

        history_ns.append(obs.north_queue + obs.south_queue)
        history_ew.append(obs.east_queue + obs.west_queue)
        rewards_history.append(current_result.reward)

        yield update_ui(current_result, direction)

        time.sleep(speed)

        if current_result.done:
            break


def stop():
    global running
    running = False


# =========================
# UI UPDATE
# =========================
def update_ui(result, direction):
    obs = result.observation

    frames = []
    for i in range(5):
        frames.append(draw(obs, direction, i))

    stats = f"""
### 📊 Stats
Step: {step_count}  
Reward: {result.reward:.3f}  
Done: {result.done}
"""

    if result.done:
        total_reward = sum(rewards_history)
        score = max(0.0, min(total_reward / 20.0, 1.0))

        final_text = f"""
### 🏁 FINAL RESULT

success: {"true" if score >= 0.5 else "false"}  
steps: {step_count}  
score: {score:.3f}  

rewards:
{[round(r, 2) for r in rewards_history]}
"""
    else:
        final_text = "### ⏳ Running..."

    return frames, stats, final_text, plot_graph()


# =========================
# UI
# =========================
with gr.Blocks() as demo:

    gr.Markdown("# 🚦 AI-Powered Smart Intersection Control System")
    gr.Markdown("### Smart City Traffic Optimization using AI + RL")

    animation = gr.HTML()
    stats = gr.Markdown()
    final_output = gr.Markdown()
    plot = gr.Plot()

    # ✅ NEW DROPDOWN
    difficulty = gr.Dropdown(
        ["easy", "medium", "hard"],
        value="medium",
        label="Difficulty Level"
    )

    with gr.Row():
        direction = gr.Radio(["NS", "EW"], value="NS")
        duration = gr.Slider(5, 60, value=30)

    with gr.Row():
        step_btn = gr.Button("▶ Step")
        auto_btn = gr.Button("🤖 Auto Play")
        stop_btn = gr.Button("⏹ Stop")
        reset_btn = gr.Button("🔄 Reset")

    speed = gr.Slider(0.1, 1.0, value=0.3, label="Speed")

    # BUTTON ACTIONS
    step_btn.click(step_env, [direction, duration],
                   [animation, stats, final_output, plot])

    auto_btn.click(auto_play, inputs=[speed],
                   outputs=[animation, stats, final_output, plot])

    stop_btn.click(stop)

    reset_btn.click(
        reset_env,
        inputs=[difficulty],
        outputs=[animation, stats, final_output, plot]
    )

    demo.load(
        reset_env,
        inputs=[difficulty],
        outputs=[animation, stats, final_output, plot]
    )


if __name__ == "__main__":
    demo.launch()