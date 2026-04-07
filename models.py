import random
from typing import Dict
from openenv.core.env_server.types import Action, Observation
from pydantic import Field

# =========================
# ACTION
# =========================
class TrafficAction(Action):
    direction: str = Field(..., description='"NS" or "EW"')
    duration: int = Field(..., description='seconds (5–60)')


# =========================
# OBSERVATION
# =========================
class TrafficObservation(Observation):
    north_queue: int = Field(default=0)
    south_queue: int = Field(default=0)
    east_queue: int = Field(default=0)
    west_queue: int = Field(default=0)

    north_wait: float = Field(default=0.0)
    south_wait: float = Field(default=0.0)
    east_wait: float = Field(default=0.0)
    west_wait: float = Field(default=0.0)

    emergency_north: bool = Field(default=False)
    emergency_south: bool = Field(default=False)
    emergency_east: bool = Field(default=False)
    emergency_west: bool = Field(default=False)


# =========================
# INTERNAL STATE
# =========================
class TrafficState:
    def __init__(self):
        self.queues: Dict[str, int] = {
            "N": random.randint(5, 20),
            "S": random.randint(5, 20),
            "E": random.randint(5, 20),
            "W": random.randint(5, 20),
        }
        self.wait_times: Dict[str, float] = {
            k: random.uniform(0, 10) for k in self.queues
        }
        self.emergency: Dict[str, bool] = {
            k: random.random() < 0.1 for k in self.queues
        }
        self.step_count = 0


# =========================
# ENVIRONMENT
# =========================
class SmartTrafficEnv:

    def __init__(self):
        self.state = TrafficState()
        self.max_steps = 20

    async def reset(self):
        self.state = TrafficState()
        self.last_direction = None
        return self._build_result(0.0, False)

    async def step(self, action: TrafficAction):
        if action is None:
            action = TrafficAction(direction="NS", duration=20)

        reward = 0.0
        done = False

        direction = action.direction.upper()
        if direction not in ["NS", "EW"]:
            reward -= 1.0
            direction = "NS"

        duration = max(5, min(action.duration, 60))
        lanes = ["N", "S"] if direction == "NS" else ["E", "W"]

        cleared = 0
        emergency_bonus = 0

        # =========================
        # CLEAR TRAFFIC
        # =========================
        for lane in lanes:
            cars_cleared = min(self.state.queues[lane], duration // 2)
            self.state.queues[lane] -= cars_cleared
            cleared += cars_cleared

            # emergency priority
            if self.state.emergency[lane]:
                emergency_bonus += 15   # 🔥 stronger boost
                self.state.emergency[lane] = False

            # reset wait time after clearing
            self.state.wait_times[lane] *= 0.5

        # =========================
        # INCOMING TRAFFIC
        # =========================
        for lane in self.state.queues:
            incoming = random.randint(1, 5)
            self.state.queues[lane] += incoming

            # increase wait time more realistically
            self.state.wait_times[lane] += 1.0 + (self.state.queues[lane] * 0.05)

            if random.random() < 0.05:
                self.state.emergency[lane] = True

        # =========================
        # REWARD CALCULATION
        # =========================
        total_wait = sum(self.state.wait_times.values())
        total_queue = sum(self.state.queues.values())

        # reward throughput
        reward += cleared * 0.6

        # reward emergency handling
        reward += emergency_bonus

        # penalize congestion
        reward -= total_queue * 0.03

        # 🔥 STRONG wait penalty (important)
        reward -= total_wait * 0.06

        # 🔥 imbalance penalty
        imbalance = abs(
            (self.state.queues["N"] + self.state.queues["S"]) -
            (self.state.queues["E"] + self.state.queues["W"])
        )
        reward -= imbalance * 0.03

        # 🔥 repetition penalty
        if self.last_direction == direction:
            reward -= 0.25

        self.last_direction = direction

        # =========================
        # NORMALIZE
        # =========================
        reward = max(min(reward / 60.0, 1.0), -1.0)

        # =========================
        # DONE CONDITION
        # =========================
        self.state.step_count += 1
        if self.state.step_count >= self.max_steps:
            done = True

        return self._build_result(reward, done)

    def get_state(self):
        return self.state

    def _build_result(self, reward, done):
        obs = TrafficObservation(
            north_queue=self.state.queues["N"],
            south_queue=self.state.queues["S"],
            east_queue=self.state.queues["E"],
            west_queue=self.state.queues["W"],
            north_wait=self.state.wait_times["N"],
            south_wait=self.state.wait_times["S"],
            east_wait=self.state.wait_times["E"],
            west_wait=self.state.wait_times["W"],
            emergency_north=self.state.emergency["N"],
            emergency_south=self.state.emergency["S"],
            emergency_east=self.state.emergency["E"],
            emergency_west=self.state.emergency["W"],
        )

        return type(
            "StepResult",
            (),
            {"observation": obs, "reward": reward, "done": done}
        )()