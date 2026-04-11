from typing import Dict
from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from models import TrafficAction, TrafficObservation


class SmartTrafficClient(
    EnvClient[TrafficAction, TrafficObservation, State]
):

    def _step_payload(self, action: TrafficAction) -> Dict:
        return {
            "signal_phase": action.signal_phase,
        }

    def _parse_result(self, payload: Dict) -> StepResult[TrafficObservation]:

        obs_data = payload.get("observation", {})

        observation = TrafficObservation(
            north_queue=obs_data.get("north_queue", 0),
            south_queue=obs_data.get("south_queue", 0),
            east_queue=obs_data.get("east_queue", 0),
            west_queue=obs_data.get("west_queue", 0),
            emergency_waiting=obs_data.get("emergency_waiting", False),
            total_queue=obs_data.get("total_queue", 0),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )