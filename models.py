from pydantic import BaseModel
import random

# -----------------------------
# ACTION, RESET & OBSERVATION MODELS
# -----------------------------
class TrafficAction(BaseModel):
    signal_phase: int  # 0 = NS, 1 = EW

# FIX: Create a Pydantic model for the Reset action so the default web UI renders an input box
class TrafficResetConfig(BaseModel):
    task: str = "medium"  # User can type 'easy', 'medium', or 'hard'

class TrafficObservation(BaseModel):
    north_queue: int
    south_queue: int
    east_queue: int
    west_queue: int
    emergency_waiting: bool
    total_queue: int
    episode_id: str = "1"
    step_count: int = 0

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
    # FIX: Accept the Pydantic config model, but allow it to be None so the inference script doesn't crash
    def reset(self, config: TrafficResetConfig = None):
        if config is None:
            config = TrafficResetConfig(task="medium")
            
        task = config.task.lower()

        if task == "easy":
            self.arrival_range = (0, 2)
            self.north = random.randint(2, 8)
            self.south = random.randint(2, 8)
            self.east = random.randint(2, 8)
            self.west = random.randint(2, 8)
            self.emergency = False

        elif task == "hard":
            self.arrival_range = (3, 8)
            self.north = random.randint(15, 25)
            self.south = random.randint(15, 25)
            self.east = random.randint(15, 25)
            self.west = random.randint(15, 25)
            self.emergency = True

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

        # arrivals
        self.north += random.randint(*self.arrival_range)
        self.south += random.randint(*self.arrival_range)
        self.east += random.randint(*self.arrival_range)
        self.west += random.randint(*self.arrival_range)

        # signal effect
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
    # ASYNC WRAPPERS (CRITICAL)
    # -----------------------------
    # FIX: Expose the config parameter to the async wrapper for the web UI
    async def reset_async(self, config: TrafficResetConfig = None):
        if config is None:
            config = TrafficResetConfig(task="medium")
            
        obs = self.reset(config)
        return TrafficStepResult(
            observation=obs,
            reward=0.0,
            done=False,
            info={},
            episode_id="1"
        )

    async def step_async(self, action: TrafficAction):
        return self.step(action)