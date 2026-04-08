from fastapi import FastAPI
from env.aare_env import AAREEnv
from models.action import AAREAction
import uvicorn

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


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()