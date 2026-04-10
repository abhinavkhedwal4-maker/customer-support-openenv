from typing import Optional
from env.models import Observation, Action, Reward
from env.tasks import TASKS


class CustomerSupportEnv:
    """
    OpenEnv-style environment for customer-support simulations.

    Lifecycle
    ---------
    obs  = env.reset(difficulty)
    obs, reward, done = env.step(action)
    info = env.state()
    """

    def __init__(self):
        self._difficulty: Optional[str] = None
        self._observation: Optional[Observation] = None
        self._last_reward: Optional[Reward] = None
        self._done: bool = False
        self._step_count: int = 0

    # ── Public API ─────────────────────────────────────────────────────────────

    def reset(self, difficulty: str = "easy") -> Observation:
        if difficulty not in TASKS:
            raise ValueError(f"Unknown difficulty '{difficulty}'. Choose from {list(TASKS.keys())}.")

        task_data, _ = TASKS[difficulty]
        self._difficulty = difficulty
        self._done = False
        self._step_count = 0
        self._last_reward = None

        self._observation = Observation(
            task_id=task_data["task_id"],
            difficulty=task_data["difficulty"],
            customer_message=task_data["customer_message"],
            context=task_data.get("context", {}),
            step=0,
            done=False,
        )
        return self._observation

    def step(self, action: Action) -> tuple[Observation, Reward, bool]:
        if self._observation is None:
            raise RuntimeError("Call reset() before step().")
        if self._done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")

        _, grader = TASKS[self._difficulty]
        reward = grader(action)

        self._step_count += 1
        self._last_reward = reward
        self._done = True          # single-turn tasks resolve in one step

        self._observation = Observation(
            task_id=self._observation.task_id,
            difficulty=self._difficulty,
            customer_message=self._observation.customer_message,
            context=self._observation.context,
            step=self._step_count,
            done=self._done,
        )
        return self._observation, reward, self._done

    def state(self) -> dict:
        return {
            "difficulty": self._difficulty,
            "step": self._step_count,
            "done": self._done,
            "last_score": self._last_reward.score if self._last_reward else None,
            "last_passed": self._last_reward.passed if self._last_reward else None,
        }