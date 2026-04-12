ATTACK_SEQUENCE = [
    "sql_injection",
    "sql_injection",
    "sql_injection"
]

class EasyTask:

    name = "easy"
    grader = "graders.grader:AAREGrader"

    def __init__(self):
        self.attack_sequence = ATTACK_SEQUENCE