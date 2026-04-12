from pydantic import BaseModel
import random

# -----------------------------
# STRICT OPENENV MODELS
# -----------------------------
class TrafficAction(BaseModel):
    signal_phase: int  # 0 = NS, 1 = EW

class TrafficResetConfig(BaseModel):
    task: str = "medium"

class TrafficObservation(BaseModel):
    north_queue: int
    south_queue: int
    east_queue: int
    west_queue: int
    emergency_waiting: bool
    total_queue: int
    episode_id: str = "1"
    step_count: int = 0
    # Keeps the Web UI stable without breaking the auto-grader
    reward: float = 0.0
    done: bool = False

class TrafficStepResult(BaseModel):
    observation: TrafficObservation
    reward: float
    done: bool
    info: dict
    episode_id: str = "1"

# -----------------------------
# ENVIRONMENT
# -----------------------------
class SmartTrafficEnv:

    def __init__(self):
        self.max_queue = 50
        self.steps = 0
        self.reset()

    # -----------------------------
    # RESET
    # -----------------------------
    # FIX: Bulletproof reset that accepts ANY input (string, Pydantic model, or None)
    def reset(self, config=None):
        if isinstance(config, str):
            task = config.lower()
        elif hasattr(config, "task"):
            task = config.task.lower()
        elif isinstance(config, dict) and "task" in config:
            task = config["task"].lower()
        else:
            task = "medium"

        if task == "easy":
            self.arrival_range = (0, 2)
        elif task == "hard":
            self.arrival_range = (3, 8)
        else:
            self.arrival_range = (0, 5)

        self.north = random.randint(5, 15)
        self.south = random.randint(5, 15)
        self.east = random.randint(5, 15)
        self.west = random.randint(5, 15)
        self.emergency = random.choice([True, False])

        self.steps = 0
        return self.get_state()

    # -----------------------------
    # STATE
    # -----------------------------
    def get_state(self):
        total = self.north + self.south + self.east + self.west

        return TrafficObservation(
            north_queue=self.north,
            south_queue=self.south,
            east_queue=self.east,
            west_queue=self.west,
            emergency_waiting=self.emergency,
            total_queue=total,
            episode_id="1",
            step_count=self.steps
        )

    @property
    def state(self):
        return self.get_state()

    # -----------------------------
    # STEP
    # -----------------------------
    def step(self, action: TrafficAction):
        self.steps += 1

        self.north += random.randint(*self.arrival_range)
        self.south += random.randint(*self.arrival_range)
        self.east += random.randint(*self.arrival_range)
        self.west += random.randint(*self.arrival_range)

        if action.signal_phase == 0:
            self.north -= min(self.north, 10)
            self.south -= min(self.south, 10)
        else:
            self.east -= min(self.east, 10)
            self.west -= min(self.west, 10)

        total = self.north + self.south + self.east + self.west

        reward = max(0.0, min(1.0, 1 - total / 200))
        done = self.steps >= 50

        return TrafficStepResult(
            observation=self.get_state(),
            reward=reward,
            done=done,
            info={
                "score": reward,
                "success": reward > 0.7
            },
            episode_id="1"
        )

    # -----------------------------
    # ASYNC WRAPPERS (FOR THE API GRADER)
    # -----------------------------
    # FIX: MUST accept 'config' so the FastAPI server doesn't crash with a TypeError!
    async def reset_async(self, config: TrafficResetConfig = None):
        return self.reset(config)

    async def step_async(self, action: TrafficAction):
        return self.step(action)