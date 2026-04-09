import random
from openenv.core.env_server.types import Action, Observation, StepResult
from pydantic import Field


# =========================
# ACTION
# =========================
class TrafficAction(Action):
    direction: str = Field(..., description="NS or EW")
    duration: int = Field(..., description="seconds")


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
# ENVIRONMENT
# =========================
class SmartTrafficEnv:

    def __init__(self):
        self.reset_internal()

    def reset_internal(self):
        self.queues = {
            "N": random.randint(5, 20),
            "S": random.randint(5, 20),
            "E": random.randint(5, 20),
            "W": random.randint(5, 20),
        }

        self.wait = {k: random.uniform(0, 10) for k in self.queues}
        self.steps = 0
        self.max_steps = 20

    # ✅ REQUIRED
    async def reset_async(self):
        self.reset_internal()
        return self._result(0.0, False)

    # ✅ REQUIRED
    async def step_async(self, action: TrafficAction):

        direction = action.direction.upper()
        duration = max(5, min(action.duration, 60))

        lanes = ["N", "S"] if direction == "NS" else ["E", "W"]

        cleared = 0

        for lane in lanes:
            cars = min(self.queues[lane], duration // 2)
            self.queues[lane] -= cars
            cleared += cars
            self.wait[lane] *= 0.5

        for lane in self.queues:
            self.queues[lane] += random.randint(1, 5)
            self.wait[lane] += 1

        reward = cleared - sum(self.queues.values()) * 0.1

        self.steps += 1
        done = self.steps >= self.max_steps

        return self._result(reward, done)

    # ✅ REQUIRED (for "Get State" button)
    def get_state(self):
        return self._observation()

    # =========================
    # HELPERS
    # =========================
    def _observation(self):
        return TrafficObservation(
            north_queue=self.queues["N"],
            south_queue=self.queues["S"],
            east_queue=self.queues["E"],
            west_queue=self.queues["W"],
            north_wait=self.wait["N"],
            south_wait=self.wait["S"],
            east_wait=self.wait["E"],
            west_wait=self.wait["W"],
        )

    def _result(self, reward, done):
        return StepResult(
            observation=self._observation(),
            reward=reward,
            done=done,
        )