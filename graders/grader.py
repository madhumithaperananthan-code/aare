class AAREGrader:

    def __init__(self):
        self.total_attacks = 0
        self.blocked_attacks = 0

    def record_step(self, attack_blocked):
        self.total_attacks += 1

        if attack_blocked:
            self.blocked_attacks += 1

    def get_score(self):

        if self.total_attacks == 0:
            return 0.5   # safe neutral score

        score = self.blocked_attacks / self.total_attacks

        # ensure score is strictly between (0,1)
        if score <= 0:
            score = 0.1
        elif score >= 1:
            score = 0.9

        return score