from openenv.core.env_server import create_fastapi_app

from env.aare_env import AAREEnv
from models.action import AAREAction
from models.observation import AAREObservation


app = create_fastapi_app(
    AAREEnv,
    AAREAction,
    AAREObservation
)