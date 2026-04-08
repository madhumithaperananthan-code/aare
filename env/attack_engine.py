import random


ATTACK_DEFENSE_MAP = {
    "sql_injection": "sanitize_queries",
    "xss": "enable_input_validation",
    "brute_force_login": "add_rate_limiting",
    "privilege_escalation": "patch_authentication",
    "insecure_file_upload": "secure_file_upload",
    "rate_limit_bypass": "enable_waf"
}


ATTACK_CHAINS = [
    ["sql_injection", "privilege_escalation"],
    ["brute_force_login", "rate_limit_bypass"],
    ["xss", "insecure_file_upload"]
]


class AttackEngine:

    def __init__(self):

        self.current_chain = random.choice(ATTACK_CHAINS)
        self.chain_index = 0

    def generate_attack(self):

        attack = self.current_chain[self.chain_index]

        if self.chain_index < len(self.current_chain) - 1:
            self.chain_index += 1

        return attack

    def check_defense(self, attack, action):

        correct_defense = ATTACK_DEFENSE_MAP.get(attack)

        return action == correct_defense

    def reset_chain(self):

        self.current_chain = random.choice(ATTACK_CHAINS)
        self.chain_index = 0