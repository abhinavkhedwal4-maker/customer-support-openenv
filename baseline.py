"""
Baseline agent — deterministic rule-based responses for each difficulty.
Run:  python baseline.py
"""

from env import CustomerSupportEnv, Action

env = CustomerSupportEnv()

# ─── Baseline responses ────────────────────────────────────────────────────────
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

# ─── Run all difficulties ──────────────────────────────────────────────────────
difficulties = ["easy", "medium", "hard"]

print("=" * 60)
print("  Customer Support OpenEnv — Baseline Agent Results")
print("=" * 60)

for diff in difficulties:
    obs = env.reset(difficulty=diff)
    print(f"\n[{diff.upper()} TASK]  task_id={obs.task_id}")
    print(f"  Customer : {obs.customer_message[:80]}...")

    action = BASELINE_RESPONSES[diff]
    print(f"  Agent    : {action.response[:80]}...")

    _, reward, done = env.step(action)

    print(f"  Score    : {reward.score:.3f}  |  Passed: {reward.passed}")
    print(f"  Feedback : {reward.feedback}")
    print(f"  Breakdown: {reward.breakdown}")
    print(f"  State    : {env.state()}")

print("\n" + "=" * 60)
print("  Done.")
print("=" * 60)