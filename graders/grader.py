# class AAREGrader:

#     def __init__(self):
#         self.total_attacks = 0
#         self.blocked_attacks = 0

#     def record_step(self, attack_blocked):
#         self.total_attacks += 1

#         if attack_blocked:
#             self.blocked_attacks += 1

#     def get_score(self):

#         if self.total_attacks == 0:
#             return 0.5   # safe neutral score

#         score = self.blocked_attacks / self.total_attacks

#         # ensure score is strictly between (0,1)
#         if score <= 0:
#             score = 0.1
#         elif score >= 1:
#             score = 0.9

#         return score

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
            return 0.5

        score = self.blocked_attacks / self.total_attacks

        if score <= 0:
            score = 0.1
        elif score >= 1:
            score = 0.9

        return score


def _extract_steps(*candidates):
    for candidate in candidates:
        if not candidate:
            continue

        if isinstance(candidate, list):
            return candidate

        if isinstance(candidate, tuple):
            return list(candidate)

        if isinstance(candidate, dict):
            for key in ("steps", "trajectory", "records", "history"):
                value = candidate.get(key)
                if isinstance(value, list):
                    return value

    return []


def _extract_attack_blocked(step):
    if isinstance(step, bool):
        return step

    if not isinstance(step, dict):
        return False

    if "attack_blocked" in step:
        return bool(step["attack_blocked"])

    info = step.get("info")
    if isinstance(info, dict) and "attack_blocked" in info:
        return bool(info["attack_blocked"])

    metadata = step.get("metadata")
    if isinstance(metadata, dict) and "attack_blocked" in metadata:
        return bool(metadata["attack_blocked"])

    return False


def grade(trajectory=None, **kwargs):
    grader = AAREGrader()
    steps = _extract_steps(
        trajectory,
        kwargs.get("trajectory"),
        kwargs.get("steps"),
        kwargs.get("records"),
        kwargs,
    )

    for step in steps:
        grader.record_step(_extract_attack_blocked(step))

    return grader.get_score()
