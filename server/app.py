from fastapi import FastAPI
from env.aare_env import AAREEnv
from models.action import AAREAction

app = FastAPI()
env = AAREEnv()

@app.get("/")
def root():
    return {"message": "AARE environment running"}

@app.api_route("/reset", methods=["GET", "POST"])
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step(action: dict):
    act = AAREAction(**action)
    observation, reward, done, info = env.step(act)

    return {
        "observation": observation.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }