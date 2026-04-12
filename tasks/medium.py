ATTACK_SEQUENCE = [
    "sql_injection",
    "brute_force_login",
    "sql_injection"
]

class MediumTask:

    name = "medium"
    grader = "graders.grader:AAREGrader"

    def __init__(self):
        self.attack_sequence = ATTACK_SEQUENCE