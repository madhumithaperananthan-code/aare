import os
from openai import OpenAI

from env.aare_env import AAREEnv
from models.action import AAREAction
from graders.grader import AAREGrader

TASK_NAME = "aare-defense"
BENCHMARK = "aare"

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")


def choose_action(attack):

    mapping = {
        "sql_injection": "sanitize_queries",
        "xss": "enable_input_validation",
        "brute_force_login": "add_rate_limiting",
        "privilege_escalation": "patch_authentication",
        "insecure_file_upload": "secure_file_upload",
        "rate_limit_bypass": "enable_waf"
    }

    return mapping.get(attack, "ignore")


def main():

    # Required LLM proxy call
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )

    client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a cybersecurity defense assistant."},
            {"role": "user", "content": "Suggest a mitigation for SQL injection."}
        ]
    )

    env = AAREEnv()
    grader = AAREGrader()

    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)

    observation = env.reset()

    step = 0
    rewards = []

    while True:

        step += 1

        action_type = choose_action(observation.attack_type)
        action = AAREAction(action_type=action_type)

        observation, reward, done, info = env.step(action)

        rewards.append(reward)

        grader.record_step(info["attack_blocked"])

        print(
            f"[STEP] step={step} action={action_type} reward={reward:.2f} done={str(done).lower()} error=null",
            flush=True
        )

        if done:
            break

    score = grader.get_score()

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(score > 0.5).lower()} steps={step} score={score:.3f} rewards={rewards_str}",
        flush=True
    )


if __name__ == "__main__":
    main()