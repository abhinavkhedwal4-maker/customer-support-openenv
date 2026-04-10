from env import CustomerSupportEnv, Action

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


def run_inference(difficulty: str = "easy") -> dict:
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
    for diff in ["easy", "medium", "hard"]:
        result = run_inference(diff)
        print(result)