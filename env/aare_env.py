# import random

# from env.attack_engine import AttackEngine
# from env.app_state import ApplicationState

# from models.observation import AAREObservation
# from openenv.core.env_server import Environment

# COMPROMISE_THRESHOLD = 0.9

# # Attack sequences MUST match tasks
# TASK_ATTACKS = {
#     "easy": [
#         "sql_injection",
#         "sql_injection",
#         "sql_injection"
#     ],
#     "medium": [
#         "sql_injection",
#         "brute_force_login",
#         "sql_injection"
#     ],
#     "hard": [
#         "xss",
#         "privilege_escalation",
#         "insecure_file_upload",
#         "rate_limit_bypass",
#         "xss"
#     ]
# }

# ATTACK_SEVERITY = {
#     "sql_injection": 0.6,
#     "xss": 0.4,
#     "brute_force_login": 0.3,
#     "privilege_escalation": 0.8,
#     "insecure_file_upload": 0.7,
#     "rate_limit_bypass": 0.5
# }


# class AAREEnv(Environment):
#     TASKS = {
#         "easy": "tasks.easy:EasyTask",
#         "medium": "tasks.medium:MediumTask",
#         "hard": "tasks.hard:HardTask"
#     }

#     def __init__(self):

#         self.attack_engine = AttackEngine()
#         self.app_state = ApplicationState()

#         self.current_attack = None
#         self.attack_sequence = []
#         self.sequence_index = 0

#         self.max_steps = 8
#         self.step_count = 0

#     def reset(self, task: str = "easy"):

#         self.task = task

#         self.app_state.reset()
#         self.attack_engine.reset_chain()

#         self.step_count = 0

#         self.attack_sequence = TASK_ATTACKS.get(task, TASK_ATTACKS["easy"])
#         self.sequence_index = 0

#         self.max_steps = len(self.attack_sequence)

#         self.current_attack = self.attack_sequence[self.sequence_index]

#         return self._get_observation()

#     def step(self, action):

#         self.step_count += 1

#         action_type = action.action_type

#         # apply defense
#         self.app_state.apply_defense(action_type)

#         # check if defense is correct
#         attack_blocked = self.attack_engine.check_defense(
#             self.current_attack,
#             action_type
#         )

#         # reward logic
#         if attack_blocked:

#             reward = 1.0

#             self.app_state.failed_attack_streak += 1

#             # reduce system risk
#             self.app_state.decrease_risk(0.1)

#         elif action_type == "ignore":

#             reward = -1.0

#             self.app_state.failed_attack_streak = 0

#             # ignoring attack increases risk more
#             self.app_state.increase_risk(0.2)

#         else:

#             reward = -0.3

#             self.app_state.failed_attack_streak = 0

#             self.app_state.increase_risk(0.1)

#         done = False

#         # success condition
#         if self.app_state.failed_attack_streak >= 3:
#             done = True

#         # failure condition
#         if self.app_state.risk_score >= COMPROMISE_THRESHOLD:
#             done = True

#         # max step condition
#         if self.step_count >= self.max_steps:
#             done = True

#         # move to next attack
#         self.sequence_index += 1

#         if self.sequence_index < len(self.attack_sequence):
#             self.current_attack = self.attack_sequence[self.sequence_index]
#         else:
#             done = True

#         observation = self._get_observation()

#         info = {
#             "attack_blocked": attack_blocked,
#             "risk_score": self.app_state.risk_score
#         }

#         return observation, reward, done, info

#     @property
#     def state(self):

#         return {
#             "defenses": self.app_state.defenses,
#             "failed_attack_streak": self.app_state.failed_attack_streak,
#             "risk_score": self.app_state.risk_score
#         }

#     def _get_observation(self):

#         return AAREObservation(
#             attack_type=self.current_attack,
#             target_component="web_app",
#             severity=ATTACK_SEVERITY[self.current_attack],
#             vulnerabilities=[self.current_attack],
#             defense_status=self.app_state.defenses,
#             failed_attack_streak=self.app_state.failed_attack_streak,
#             risk_score=self.app_state.risk_score
#         )
from env.attack_engine import AttackEngine
from env.app_state import ApplicationState
from models.observation import AAREObservation
from openenv.core.env_server import Environment

COMPROMISE_THRESHOLD = 0.9

TASKS_CONFIG = {
    "easy": {
        "id": "easy",
        "name": "easy",
        "difficulty": "easy",
        "description": "Defend against repeated SQL injection attacks.",
        "path": "tasks.easy:EasyTask",
        "grader": "graders.grader:grade",
        "success_threshold": 0.6,
        "attack_sequence": [
            "sql_injection",
            "sql_injection",
            "sql_injection",
        ],
    },
    "medium": {
        "id": "medium",
        "name": "medium",
        "difficulty": "medium",
        "description": "Defend against SQL injection and brute-force login attacks.",
        "path": "tasks.medium:MediumTask",
        "grader": "graders.grader:grade",
        "success_threshold": 0.6,
        "attack_sequence": [
            "sql_injection",
            "brute_force_login",
            "sql_injection",
            "brute_force_login",
        ],
    },
    "hard": {
        "id": "hard",
        "name": "hard",
        "difficulty": "hard",
        "description": "Defend against multiple attack types in sequence.",
        "path": "tasks.hard:HardTask",
        "grader": "graders.grader:grade",
        "success_threshold": 0.6,
        "attack_sequence": [
            "xss",
            "privilege_escalation",
            "insecure_file_upload",
            "rate_limit_bypass",
            "xss",
        ],
    },
}

ATTACK_SEVERITY = {
    "sql_injection": 0.6,
    "xss": 0.4,
    "brute_force_login": 0.3,
    "privilege_escalation": 0.8,
    "insecure_file_upload": 0.7,
    "rate_limit_bypass": 0.5,
}


class AAREEnv(Environment):
    TASKS = {task_name: config["path"] for task_name, config in TASKS_CONFIG.items()}

    def __init__(self):
        super().__init__()
        self.attack_engine = AttackEngine()
        self.app_state = ApplicationState()

        self.task = "easy"
        self.current_attack = None
        self.attack_sequence = []
        self.sequence_index = 0

        self.max_steps = 8
        self.step_count = 0

    def reset(self, seed=None, episode_id=None, task="easy", task_id=None, **kwargs):
        selected_task = task_id or kwargs.get("task_id") or kwargs.get("task") or task or "easy"
        if selected_task not in TASKS_CONFIG:
            selected_task = "easy"

        self.task = selected_task

        self.app_state.reset()
        self.attack_engine.reset_chain()
        self.step_count = 0

        self.attack_sequence = list(TASKS_CONFIG[selected_task]["attack_sequence"])
        self.sequence_index = 0
        self.max_steps = len(self.attack_sequence)
        self.current_attack = self.attack_sequence[self.sequence_index]

        observation = self._get_observation()
        observation.done = False
        observation.reward = 0.0
        observation.metadata = {"task": self.task}
        return observation

    def step(self, action, timeout_s=None, **kwargs):
        self.step_count += 1
        action_type = action.action_type

        self.app_state.apply_defense(action_type)

        attack_blocked = self.attack_engine.check_defense(
            self.current_attack,
            action_type,
        )

        if attack_blocked:
            reward = 1.0
            self.app_state.failed_attack_streak += 1
            self.app_state.decrease_risk(0.1)
        elif action_type == "ignore":
            reward = -1.0
            self.app_state.failed_attack_streak = 0
            self.app_state.increase_risk(0.2)
        else:
            reward = -0.3
            self.app_state.failed_attack_streak = 0
            self.app_state.increase_risk(0.1)

        done = False

        if self.app_state.failed_attack_streak >= 3:
            done = True

        if self.app_state.risk_score >= COMPROMISE_THRESHOLD:
            done = True

        if self.step_count >= self.max_steps:
            done = True

        self.sequence_index += 1

        if self.sequence_index < len(self.attack_sequence):
            self.current_attack = self.attack_sequence[self.sequence_index]
        else:
            done = True

        info = {
            "task": self.task,
            "attack_blocked": attack_blocked,
            "risk_score": self.app_state.risk_score,
        }

        observation = self._get_observation()
        observation.reward = reward
        observation.done = done
        observation.metadata = info

        return observation, reward, done, info

    @property
    def state(self):
        return {
            "task": self.task,
            "defenses": self.app_state.defenses,
            "failed_attack_streak": self.app_state.failed_attack_streak,
            "risk_score": self.app_state.risk_score,
        }

    def _get_observation(self):
        return AAREObservation(
            attack_type=self.current_attack,
            target_component="web_app",
            severity=ATTACK_SEVERITY[self.current_attack],
            vulnerabilities=[self.current_attack],
            defense_status=self.app_state.defenses,
            failed_attack_streak=self.app_state.failed_attack_streak,
            risk_score=self.app_state.risk_score,
        )
