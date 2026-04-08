from pydantic import BaseModel
from typing import List, Dict


class AAREObservation(BaseModel):

    attack_type: str
    target_component: str
    severity: float
    vulnerabilities: List[str]
    defense_status: Dict[str, bool]
    failed_attack_streak: int

    # NEW FIELD
    risk_score: float