from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from env import CustomerSupportEnv, Action
import uvicorn

app = FastAPI(title="Customer Support OpenEnv")
env = CustomerSupportEnv()

BASELINE_RESPONSES = {
    "easy": Action(
        response=(
            "Of course! I'm happy to help you reset your password. "
            "Please check your email inbox — we'll send you a secure reset link right away. "
            "If you don't see it within a few minutes, check your spam folder."
        ),
        action_type="reply",
    ),
    "medium": Action(
        response=(
            "I sincerely apologize for the duplicate charge on order #A8821. "
            "I can see a billing error occurred and you are absolutely eligible for a full refund. "
            "I'm processing that now and you should see the credit within 3–5 business days. "
            "Thank you for your patience."
        ),
        action_type="refund",
    ),
    "hard": Action(
        response=(
            "I sincerely apologize for everything you've experienced — this is completely unacceptable "
            "and I personally take ownership of getting this resolved today. "
            "Your account was suspended due to a payment processing issue, which we will fix immediately. "
            "Your data is fully recoverable and I'm escalating this to a dedicated team lead right now. "
            "You will receive a direct call within 2 hours with a full resolution. "
            "You have my word."
        ),
        action_type="escalate",
    ),
}


class ResetRequest(BaseModel):
    difficulty: Optional[str] = "easy"


class StepRequest(BaseModel):
    response: str
    action_type: Optional[str] = "reply"


@app.get("/")
def root():
    return {"name": "customer-support-openenv", "version": "1.0.0", "status": "running"}


@app.post("/reset")
def reset(request: Optional[ResetRequest] = None):
    difficulty = request.difficulty if request else "easy"
    obs = env.reset(difficulty=difficulty)
    return obs.model_dump()


@app.post("/step")
def step(request: StepRequest):
    action = Action(response=request.response, action_type=request.action_type)
    obs, reward, done = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
    }


@app.get("/state")
def state():
    return env.state()


@app.post("/inference")
def inference(request: Optional[ResetRequest] = None):
    difficulty = request.difficulty if request else "easy"
    obs = env.reset(difficulty=difficulty)
    action = BASELINE_RESPONSES[difficulty]
    _, reward, done = env.step(action)
    return {
        "task_id": obs.task_id,
        "difficulty": difficulty,
        "score": reward.score,
        "passed": reward.passed,
        "feedback": reward.feedback,
        "breakdown": reward.breakdown,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)