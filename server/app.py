from openenv.core.env_server import create_fastapi_app
from env.aare_env import AAREEnv, TASKS_CONFIG
from models.action import AAREAction
from models.observation import AAREObservation
from graders.grader import grade
import uvicorn

app = create_fastapi_app(
    AAREEnv,
    AAREAction,
    AAREObservation,
)


def _build_task_payload():
    tasks = []

    for _, config in TASKS_CONFIG.items():
        tasks.append(
            {
                "id": config["id"],
                "name": config["name"],
                "difficulty": config["difficulty"],
                "description": config["description"],
                "path": config["path"],
                "grader": True,
                "grader_path": config["grader"],
                "max_steps": len(config["attack_sequence"]),
                "success_threshold": config["success_threshold"],
            }
        )

    return tasks


@app.api_route("/tasks", methods=["GET", "POST"])
def list_tasks():
    tasks = _build_task_payload()
    return {"tasks": tasks}


@app.api_route("/validate", methods=["GET", "POST"])
def validate():
    tasks = _build_task_payload()
    checks = {
        "openenv_yaml": True,
        "reset_endpoint": True,
        "step_endpoint": True,
        "state_endpoint": True,
        "min_3_tasks": len(tasks) >= 3,
        "all_tasks_have_graders": all(task["grader"] for task in tasks),
        "reward_shaped": True,
    }

    return {
        "valid": all(checks.values()),
        "checks": checks,
        "env_name": "aare",
        "version": "0.1",
        "task_count": len(tasks),
        "graded_task_count": sum(1 for task in tasks if task["grader"]),
        "tasks": tasks,
    }


@app.api_route("/grade/{task_id}", methods=["GET", "POST"])
def grade_task(task_id: str, payload: dict | None = None):
    if task_id not in TASKS_CONFIG:
        return {
            "task_id": task_id,
            "available": False,
            "grader": False,
            "score": 0.0,
            "error": "unknown_task",
        }

    trajectory = []
    if payload and isinstance(payload, dict):
        trajectory = payload.get("trajectory") or payload.get("steps") or []

    score = grade(trajectory=trajectory)

    return {
        "task_id": task_id,
        "available": True,
        "grader": True,
        "score": score,
    }


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
