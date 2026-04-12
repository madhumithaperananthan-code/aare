# from openenv.core.env_server import create_fastapi_app
# from env.aare_env import AAREEnv
# from models.action import AAREAction
# from models.observation import AAREObservation
# import uvicorn

# app = create_fastapi_app(
#     AAREEnv,
#     AAREAction,
#     AAREObservation
# )

# def main():
#     uvicorn.run(app, host="0.0.0.0", port=7860)


# if __name__ == "__main__":
#     main()
from openenv.core.env_server import create_fastapi_app
from env.aare_env import AAREEnv, TASKS_CONFIG
from models.action import AAREAction
from models.observation import AAREObservation
import uvicorn

app = create_fastapi_app(
    AAREEnv,
    AAREAction,
    AAREObservation,
)


def _build_task_payload():
    tasks = []

    for task_id, config in TASKS_CONFIG.items():
        tasks.append(
            {
                "id": config["id"],
                "name": config["name"],
                "difficulty": config["difficulty"],
                "description": config["description"],
                "path": config["path"],
                "grader": config["grader"],
                "has_grader": bool(config["grader"]),
                "max_steps": len(config["attack_sequence"]),
                "success_threshold": config["success_threshold"],
            }
        )

    return tasks


@app.api_route("/tasks", methods=["GET", "POST"])
def list_tasks():
    tasks = _build_task_payload()
    graded_count = sum(1 for task in tasks if task["has_grader"])

    return {
        "tasks": tasks,
        "task_count": len(tasks),
        "graded_task_count": graded_count,
    }


@app.api_route("/validate", methods=["GET", "POST"])
def validate():
    tasks = _build_task_payload()
    graded_count = sum(1 for task in tasks if task["has_grader"])

    return {
        "valid": graded_count >= 3,
        "env_name": "aare",
        "version": "0.1",
        "task_count": len(tasks),
        "graded_task_count": graded_count,
        "tasks": tasks,
    }


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
