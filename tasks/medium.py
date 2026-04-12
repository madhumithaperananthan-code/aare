ATTACK_SEQUENCE = [
    "sql_injection",
    "brute_force_login",
    "sql_injection",
    "brute_force_login",
]


class MediumTask:
    id = "medium"
    name = "medium"
    difficulty = "medium"
    description = "Defend against SQL injection and brute-force login attacks."
    grader = "graders.grader:grade"
    max_steps = len(ATTACK_SEQUENCE)
    success_threshold = 0.6

    def __init__(self):
        self.attack_sequence = ATTACK_SEQUENCE
