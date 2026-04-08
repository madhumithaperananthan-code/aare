import random

from env.attack_engine import AttackEngine
from env.app_state import ApplicationState

from models.observation import AAREObservation
COMPROMISE_THRESHOLD = 0.9

ATTACK_SEVERITY = {
    "sql_injection": 0.6,
    "xss": 0.4,
    "brute_force_login": 0.3,
    "privilege_escalation": 0.8,
    "insecure_file_upload": 0.7,
    "rate_limit_bypass": 0.5
}
class AAREEnv:

    def __init__(self):
        self.attack_engine = AttackEngine()
        self.app_state = ApplicationState()
        self.current_attack = None
        self.max_steps = 8
        self.step_count = 0
    def reset(self):
        self.app_state.reset()
        self.attack_engine.reset_chain()
        self.step_count = 0
        self.current_attack = self.attack_engine.generate_attack()
        return self._get_observation()

    def step(self, action):

        self.step_count += 1

        # apply defense
        self.app_state.apply_defense(action.action_type)

        # check attack success
        attack_blocked = self.attack_engine.check_defense(
            self.current_attack,
            action.action_type
        )

        if attack_blocked:
            reward = 1.0
            self.app_state.failed_attack_streak += 1
            self.app_state.decrease_risk(0.1)

        else:
            reward = -0.3
            self.app_state.failed_attack_streak = 0
            self.app_state.increase_risk(0.2)

        # initialize done
        done = False

        # success condition
        if self.app_state.failed_attack_streak >= 3:
            done = True

        # failure condition (system compromised)
        if self.app_state.risk_score >= COMPROMISE_THRESHOLD:
            done = True

        # max step condition
        if self.step_count >= self.max_steps:
            done = True

        # generate next attack
        self.current_attack = self.attack_engine.generate_attack()

        observation = self._get_observation()

        info = {
            "attack_blocked": attack_blocked,
            "risk_score": self.app_state.risk_score
        }

        return observation, reward, done, info

    def state(self):
        return {
        "defenses": self.app_state.defenses,
        "failed_attack_streak": self.app_state.failed_attack_streak
    }
    
    def _get_observation(self):

     return AAREObservation(
        attack_type=self.current_attack,
        target_component="web_app",
        severity=ATTACK_SEVERITY[self.current_attack],
        vulnerabilities=[self.current_attack],
        defense_status=self.app_state.defenses,
        failed_attack_streak=self.app_state.failed_attack_streak,
        risk_score=self.app_state.risk_score
     )