from openenv.core.env_server import create_fastapi_app
from env.aare_env import AAREEnv
from models.action import AAREAction
from models.observation import AAREObservation

import uvicorn

# Create the FastAPI application
app = create_fastapi_app(
    AAREEnv,
    AAREAction,
    AAREObservation
)


def main():
    """
    Entry point required by OpenEnv validator.
    Runs the FastAPI server.
    """
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()