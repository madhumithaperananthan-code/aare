from fastapi import FastAPI
from env.aare_env import AAREEnv
from models.action import AAREAction

app = FastAPI()

env = AAREEnv()

@app.get("/")
def root():
    return {"message": "AARE environment running"}

<<<<<<< HEAD
@app.api_route("/reset", methods=["GET", "POST"])
=======
@app.get("/reset")
>>>>>>> 24ed14881863be097febb4479c3ee22ea7160db3
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