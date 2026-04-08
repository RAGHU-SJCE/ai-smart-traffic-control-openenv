# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

"""
FastAPI application for the Smart Traffic Environment.
"""

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:  # pragma: no cover
    raise ImportError(
        "openenv is required for the web interface. Install dependencies with '\n    uv sync\n'"
    ) from e

# ✅ CORRECT IMPORT (clean & proper)
from models import TrafficAction, TrafficObservation, SmartTrafficEnv


# ✅ CREATE APP
app = create_app(
    SmartTrafficEnv,
    TrafficAction,
    TrafficObservation,
    env_name="ai-smart-traffic-control",
    max_concurrent_envs=1,
)


def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    main(port=args.port)