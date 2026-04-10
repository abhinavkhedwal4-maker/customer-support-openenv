from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Observation(BaseModel):
    task_id: str
    difficulty: str  # "easy" | "medium" | "hard"
    customer_message: str
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    step: int = 0
    done: bool = False


class Action(BaseModel):
    response: str
    action_type: str = "reply"  # "reply" | "escalate" | "refund" | "close"
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class Reward(BaseModel):
    score: float          # 0.0 – 1.0
    feedback: str
    passed: bool
    breakdown: Optional[Dict[str, float]] = Field(default_factory=dict)