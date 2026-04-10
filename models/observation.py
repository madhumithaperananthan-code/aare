from typing import List, Dict
from openenv.core.env_server import Observation


class AAREObservation(Observation):

    attack_type: str
    target_component: str
    severity: float
    vulnerabilities: List[str]
    defense_status: Dict[str, bool]
    failed_attack_streak: int
    risk_score: float