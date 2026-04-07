# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the Smart Traffic Environment.
"""

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:  # pragma: no cover
    raise ImportError(
        "openenv is required for the web interface. Install dependencies with '\n    uv sync\n'"
    ) from e

# --- UPDATED IMPORTS ---
# We are now importing your custom traffic classes directly from models.py
from models import TrafficAction, TrafficObservation, SmartTrafficEnv

# --- UPDATED APP CREATION ---
# Create the app with web interface and connect it to the new traffic logic
app = create_app(
    SmartTrafficEnv,
    TrafficAction,
    TrafficObservation,
    env_name="Smart_Traffic_Control",
    max_concurrent_envs=1,  # increase this number to allow more concurrent WebSocket sessions
)

def main(host: str = "0.0.0.0", port: int = 8000):
    """
    Entry point for direct execution via uv run or python -m.
    """
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    main(port=args.port)