from env.models import Action, Reward


# ─── Easy Task ────────────────────────────────────────────────────────────────
EASY_TASK = {
    "task_id": "easy-001",
    "difficulty": "easy",
    "customer_message": "Hi! I need to reset my password. Can you help?",
    "context": {"account_status": "active", "email_verified": True},
}


def grade_easy(action: Action) -> Reward:
    response_lower = action.response.lower()
    score = 0.0
    breakdown = {}

    # Check for key elements
    keyword_hits = sum([
        "password" in response_lower,
        "reset" in response_lower or "link" in response_lower,
        "email" in response_lower,
    ])
    breakdown["keywords"] = round(keyword_hits / 3, 2)

    # Polite tone
    polite = any(w in response_lower for w in ["happy to", "sure", "of course", "glad", "please"])
    breakdown["politeness"] = 1.0 if polite else 0.0

    # Reasonable length (not too short, not a wall of text)
    length_ok = 20 <= len(action.response.split()) <= 120
    breakdown["length"] = 1.0 if length_ok else 0.3

    score = round(
        breakdown["keywords"] * 0.5 +
        breakdown["politeness"] * 0.25 +
        breakdown["length"] * 0.25,
        3,
    )
    passed = score >= 0.6
    feedback = "Good password-reset guidance." if passed else "Response missing key reset instructions or too brief."
    return Reward(score=score, feedback=feedback, passed=passed, breakdown=breakdown)


# ─── Medium Task ──────────────────────────────────────────────────────────────
MEDIUM_TASK = {
    "task_id": "medium-001",
    "difficulty": "medium",
    "customer_message": (
        "I was charged twice for my subscription last month. "
        "Order #A8821. I want a refund immediately!"
    ),
    "context": {"order_id": "A8821", "duplicate_charge": True, "refund_eligible": True},
}


def grade_medium(action: Action) -> Reward:
    response_lower = action.response.lower()
    breakdown = {}

    # Acknowledge the problem
    empathy = any(w in response_lower for w in ["sorry", "apologize", "understand", "frustrating"])
    breakdown["empathy"] = 1.0 if empathy else 0.0

    # Mention refund
    mentions_refund = "refund" in response_lower
    breakdown["refund_mention"] = 1.0 if mentions_refund else 0.0

    # Reference the order
    mentions_order = "a8821" in response_lower or "order" in response_lower
    breakdown["order_reference"] = 1.0 if mentions_order else 0.0

    # Appropriate action_type
    correct_action = action.action_type in ("refund", "reply")
    breakdown["action_type"] = 1.0 if correct_action else 0.0

    score = round(
        breakdown["empathy"] * 0.25 +
        breakdown["refund_mention"] * 0.35 +
        breakdown["order_reference"] * 0.20 +
        breakdown["action_type"] * 0.20,
        3,
    )
    passed = score >= 0.65
    feedback = "Handled billing dispute well." if passed else "Must acknowledge duplicate charge and confirm refund."
    return Reward(score=score, feedback=feedback, passed=passed, breakdown=breakdown)


# ─── Hard Task ────────────────────────────────────────────────────────────────
HARD_TASK = {
    "task_id": "hard-001",
    "difficulty": "hard",
    "customer_message": (
        "This is absolutely unacceptable! My account was suspended without warning, "
        "I lost all my data, your team has ignored three of my emails, and I'm going "
        "to report this to the Better Business Bureau unless you resolve this RIGHT NOW."
    ),
    "context": {
        "account_status": "suspended",
        "suspension_reason": "payment_failure",
        "previous_contacts": 3,
        "data_recoverable": True,
    },
}


def grade_hard(action: Action) -> Reward:
    response_lower = action.response.lower()
    breakdown = {}

    # Strong empathy / de-escalation  ← UPDATED
    de_escalate = sum(
        w in response_lower
        for w in ["sincerely apologize", "truly sorry", "understand",
                  "completely", "priority", "apologize", "unacceptable"]
    )
    breakdown["de_escalation"] = min(1.0, de_escalate * 0.25)

    # Explain suspension cause
    explains_cause = any(w in response_lower for w in ["payment", "billing", "suspended"])
    breakdown["explains_cause"] = 1.0 if explains_cause else 0.0

    # Offers data recovery
    offers_recovery = any(w in response_lower for w in ["data", "recover", "restore", "retrieve"])
    breakdown["data_recovery"] = 1.0 if offers_recovery else 0.0

    # Escalation path or ownership
    takes_ownership = any(w in response_lower for w in ["escalate", "manager", "personally",
                                                         "dedicated", "team lead"])
    breakdown["ownership"] = 1.0 if takes_ownership else 0.0

    # Concrete next step
    next_step = any(w in response_lower for w in ["within", "hours", "today", "immediately",
                                                   "right now", "call", "contact"])
    breakdown["next_step"] = 1.0 if next_step else 0.0

    score = round(
        breakdown["de_escalation"] * 0.25 +
        breakdown["explains_cause"] * 0.15 +
        breakdown["data_recovery"] * 0.20 +
        breakdown["ownership"] * 0.20 +
        breakdown["next_step"] * 0.20,
        3,
    )
    passed = score >= 0.70
    feedback = (
        "Excellent crisis handling." if passed
        else "Must de-escalate, explain cause, address data recovery, and give a concrete next step."
    )
    return Reward(score=score, feedback=feedback, passed=passed, breakdown=breakdown)


# ─── Registry ─────────────────────────────────────────────────────────────────
TASKS = {
    "easy": (EASY_TASK, grade_easy),
    "medium": (MEDIUM_TASK, grade_medium),
    "hard": (HARD_TASK, grade_hard),
}