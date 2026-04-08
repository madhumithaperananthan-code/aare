ATTACK_SEQUENCE = [
    "sql_injection",
    "brute_force_login",
    "sql_injection",
    "brute_force_login"
]

class MediumTask:

    name = "medium"

    def __init__(self):
        self.attack_sequence = ATTACK_SEQUENCE