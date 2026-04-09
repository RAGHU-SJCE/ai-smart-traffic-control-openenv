import random
from typing import Dict
from openenv.core.env_server.types import Action, Observation, StepResult
from pydantic import Field


# =========================
# ACTION
# =========================
class TrafficAction(Action):
    direction: str = Field(..., description='"NS" or "EW"')
    duration: int = Field(..., description='seconds')


# =========================
# OBSERVATION
# =========================
class TrafficObservation(Observation):
    north_queue: int = 0
    south_queue: int = 0
    east_queue: int = 0
    west_queue: int = 0

    north_wait: float = 0.0
    south_wait: float = 0.0
    east_wait: float = 0.0
    west_wait: float = 0.0


# =========================
# STATE
# =========================
class TrafficState:
    def __init__(self):
        self.queues = {
            "N": random.randint(5, 20),
            "S": random.randint(5, 20),
            "E": random.randint(5, 20),
            "W": random.randint(5, 20),
        }

        self.wait = {k: random.uniform(0, 10) for k in self.queues}
        self.step_count = 0


# =========================
# ENVIRONMENT
# =========================
class SmartTrafficEnv:

    def __init__(self):
        self.state = TrafficState()
        self.max_steps = 20

    # ✅ REQUIRED
    async def reset_async(self):
        self.state = TrafficState()
        return self._build_result(0.0, False)

    # ✅ REQUIRED
    async def step_async(self, action: TrafficAction):

        direction = action.direction.upper()
        duration = max(5, min(action.duration, 60))

        lanes = ["N", "S"] if direction == "NS" else ["E", "W"]

        cleared = 0

        for lane in lanes:
            cars = min(self.state.queues[lane], duration // 2)
            self.state.queues[lane] -= cars
            cleared += cars
            self.state.wait[lane] *= 0.5

        # incoming traffic
        for lane in self.state.queues:
            self.state.queues[lane] += random.randint(1, 5)
            self.state.wait[lane] += 1

        reward = cleared - sum(self.state.queues.values()) * 0.1

        self.state.step_count += 1
        done = self.state.step_count >= self.max_steps

        return self._build_result(reward, done)

    # =========================
    # BUILD RESULT ✅ IMPORTANT
    # =========================
    def _build_result(self, reward, done):

        obs = TrafficObservation(
            north_queue=self.state.queues["N"],
            south_queue=self.state.queues["S"],
            east_queue=self.state.queues["E"],
            west_queue=self.state.queues["W"],
            north_wait=self.state.wait["N"],
            south_wait=self.state.wait["S"],
            east_wait=self.state.wait["E"],
            west_wait=self.state.wait["W"],
        )

        return StepResult(
            observation=obs,
            reward=reward,
            done=done,
        )