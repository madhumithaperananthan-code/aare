ATTACK_SEQUENCE = [
    "xss",
    "privilege_escalation",
    "insecure_file_upload",
    "rate_limit_bypass",
    "xss"
]

class HardTask:

    name = "hard"
    grader = "graders.grader:AAREGrader"

    def __init__(self):
        self.attack_sequence = ATTACK_SEQUENCE
      