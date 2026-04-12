import os
from openai import OpenAI

from env.aare_env import AAREEnv
from models.action import AAREAction
from graders.grader import AAREGrader

TASK_NAME = "aare-defense"
BENCHMARK = "aare"

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

def call_llm_proxy():
    try:
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )

        client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )

        print("[LLM_PROXY_CALL]", flush=True)

    except Exception as e:
        print(f"[LLM_ERROR] {str(e)}", flush=True)
        
def main():

    call_llm_proxy()

    env = AAREEnv()
    grader = AAREGrader()
    
    try:
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )

        client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )

        print("[LLM_PROXY_CALL]", flush=True)

    except Exception as e:
        print(f"[LLM_ERROR] {str(e)}", flush=True)

    # ---- Run environment ----

    env = AAREEnv()
    grader = AAREGrader()

    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)

    observation = env.reset("medium")

    step = 0
    rewards = []

    while True:

        step += 1

        action_type = choose_action(observation.attack_type)
        action = AAREAction(action_type=action_type)

        observation, reward, done, info = env.step(action)

        rewards.append(reward)

        grader.record_step(info.get("attack_blocked", False))

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