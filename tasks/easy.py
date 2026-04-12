# ATTACK_SEQUENCE = [
#     "sql_injection",
#     "sql_injection",
#     "sql_injection"
# ]

# class EasyTask:

#     name = "easy"
#     grader = "graders.grader:AAREGrader"

#     def __init__(self):
#         self.attack_sequence = ATTACK_SEQUENCE

ATTACK_SEQUENCE = [
    "sql_injection",
    "sql_injection",
    "sql_injection",
]


class EasyTask:
    id = "easy"
    name = "easy"
    difficulty = "easy"
    description = "Defend against repeated SQL injection attacks."
    grader = "graders.grader:grade"
    max_steps = len(ATTACK_SEQUENCE)
    success_threshold = 0.6

    def __init__(self):
        self.attack_sequence = ATTACK_SEQUENCE
