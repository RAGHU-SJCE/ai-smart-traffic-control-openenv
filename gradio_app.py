import gradio as gr
import time
from models import SmartTrafficEnv, TrafficAction

env = SmartTrafficEnv()

# Safely extract initial state
initial_state = env.reset()
state = initial_state.dict() if hasattr(initial_state, "dict") else initial_state.model_dump()
current_signal = 0

def render(obs, signal):
    # safety conversion
    if hasattr(obs, "dict"):
        obs = obs.dict()
    elif hasattr(obs, "model_dump"):
        obs = obs.model_dump()

    def cars(n, direction):
        html = ""
        for i in range(min(n, 6)):
            html += f'<div class="car {direction}" style="animation-delay:{i*0.3}s"></div>'
        return html

    signal_ns = "green" if signal == 0 else "red"
    signal_ew = "green" if signal == 1 else "red"

    return f"""
    <style>
    .road {{
        width: 400px;
        height: 400px;
        margin: auto;
        background: #2c2c2c;
        position: relative;
    }}

    .lane {{ position: absolute; display: flex; }}

    .north {{ top: 0; left: 45%; flex-direction: column; }}
    .south {{ bottom: 0; left: 45%; flex-direction: column; }}
    .east {{ right: 0; top: 45%; }}
    .west {{ left: 0; top: 45%; }}

    .car {{
        width: 15px;
        height: 25px;
        background: yellow;
        margin: 2px;
        animation: move 2s linear infinite;
    }}

    @keyframes move {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(20px); }}
    }}

    .light {{
        width: 20px;
        height: 20px;
        border-radius: 50%;
    }}

    .green {{ background: lime; }}
    .red {{ background: red; }}

    .lights {{
        position: absolute;
        top: 45%;
        left: 45%;
    }}
    </style>

    <div class="road">
        <div class="lane north">{cars(obs["north_queue"], "north")}</div>
        <div class="lane south">{cars(obs["south_queue"], "south")}</div>
        <div class="lane east">{cars(obs["east_queue"], "east")}</div>
        <div class="lane west">{cars(obs["west_queue"], "west")}</div>

        <div class="lights">
            <div class="light {signal_ns}"></div>
            <div class="light {signal_ew}"></div>
        </div>
    </div>
    """

def step_fn(action):
    global state, current_signal
    current_signal = action
    
    # Run step
    raw_result = env.step(TrafficAction(signal_phase=action))
    
    # FIX: Convert Pydantic object back to dict so Gradio can read it safely
    result = raw_result.dict() if hasattr(raw_result, "dict") else raw_result.model_dump()
    
    state = result["observation"]
    return render(state, current_signal), result

def reset_fn():
    global state
    raw_state = env.reset()
    state = raw_state.dict() if hasattr(raw_state, "dict") else raw_state.model_dump()
    return render(state, 0), state

def get_state_fn():
    return state

def autoplay_fn():
    global state, current_signal
    for _ in range(20):
        ns = state["north_queue"] + state["south_queue"]
        ew = state["east_queue"] + state["west_queue"]

        action = 0 if ns >= ew else 1

        raw_result = env.step(TrafficAction(signal_phase=action))
        result = raw_result.dict() if hasattr(raw_result, "dict") else raw_result.model_dump()
        
        state = result["observation"]

        yield render(state, action), result
        time.sleep(0.4)

# FIX: Change the block name to `interface` so OpenEnv can import it!
with gr.Blocks() as interface:
    gr.Markdown("# 🚦 Smart Traffic Simulator")

    display = gr.HTML(render(state, current_signal))
    output = gr.JSON()

    with gr.Row():
        gr.Button("Step NS").click(lambda: step_fn(0), outputs=[display, output])
        gr.Button("Step EW").click(lambda: step_fn(1), outputs=[display, output])

    with gr.Row():
        gr.Button("Reset").click(reset_fn, outputs=[display, output])
        gr.Button("Get State").click(get_state_fn, outputs=output)
        gr.Button("Autoplay").click(autoplay_fn, outputs=[display, output])