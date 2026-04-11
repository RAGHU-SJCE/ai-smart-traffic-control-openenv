from openenv.core.env_server.http_server import create_app
from models import TrafficAction, TrafficObservation, SmartTrafficEnv

import gradio as gr
# FIX: Import 'interface' instead of 'demo' to match your gradio_app.py file
from gradio_app import interface 

app = create_app(
    SmartTrafficEnv,
    TrafficAction,
    TrafficObservation,
    env_name="ai-smart-control-system",
)

# FIX: Mount the 'interface' block to the /ui path
app = gr.mount_gradio_app(app, interface, path="/ui")
