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
            return 0.0

        return self.blocked_attacks / self.total_attacks