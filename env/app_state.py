class ApplicationState:

    def __init__(self):

        self.defenses = {
            "sanitize_queries": False,
            "enable_input_validation": False,
            "add_rate_limiting": False,
            "patch_authentication": False,
            "secure_file_upload": False,
            "enable_waf": False
        }

        self.failed_attack_streak = 0

        # NEW: system risk score
        self.risk_score = 0.3

    def apply_defense(self, action):

        if action in self.defenses:
            self.defenses[action] = True

    def increase_risk(self, severity):

        self.risk_score += severity
        self.risk_score = min(self.risk_score, 1.0)

    def decrease_risk(self, amount):

        self.risk_score -= amount
        self.risk_score = max(self.risk_score, 0.0)

    def reset(self):

        for key in self.defenses:
            self.defenses[key] = False

        self.failed_attack_streak = 0
        self.risk_score = 0.3