# ATTACK_SEQUENCE = [
#     "xss",
#     "privilege_escalation",
#     "insecure_file_upload",
#     "rate_limit_bypass",
#     "xss"
# ]

# class HardTask:

#     name = "hard"
#     grader = "graders.grader:AAREGrader"

#     def __init__(self):
#         self.attack_sequence = ATTACK_SEQUENCE

ATTACK_SEQUENCE = [
    "xss",
    "privilege_escalation",
    "insecure_file_upload",
    "rate_limit_bypass",
    "xss",
]


class HardTask:
    id = "hard"
    name = "hard"
    difficulty = "hard"
    description = "Defend against multiple attack types including XSS and privilege escalation."
    grader = "graders.grader:grade"
    max_steps = len(ATTACK_SEQUENCE)
    success_threshold = 0.6

    def __init__(self):
        self.attack_sequence = ATTACK_SEQUENCE
