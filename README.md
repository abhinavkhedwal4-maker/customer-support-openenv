---
title: Customer Support OpenEnv
emoji: 🎧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# customer-support-openenv

An **OpenEnv-style** reinforcement-learning environment that simulates customer-support
interactions across three difficulty tiers: **easy**, **medium**, and **hard**.

---

## Project Structure
customer-support-openenv/
│── baseline.py          # Rule-based baseline agent
│── env/
│   ├── init.py      # Public exports
│   ├── environment.py   # CustomerSupportEnv (reset / step / state)
│   ├── models.py        # Pydantic schemas: Observation, Action, Reward
│   └── tasks.py         # Task definitions + graders
│── openenv.yaml         # Environment metadata
│── Dockerfile           # Container to run baseline
│── requirements.txt     # Python dependencies
└── README.md
---

## Tasks

| Difficulty | Task ID      | Scenario                            | Pass Threshold |
|------------|--------------|-------------------------------------|---------------|
| Easy       | `easy-001`   | Password reset request              | ≥ 0.60        |
| Medium     | `medium-001` | Duplicate billing dispute           | ≥ 0.65        |
| Hard       | `hard-001`   | Suspended account + escalation threat | ≥ 0.70      |

### Grading dimensions

**Easy** — keywords (50%), polite tone (25%), response length (25%)  
**Medium** — empathy (25%), refund mention (35%), order reference (20%), action type (20%)  
**Hard** — de-escalation (25%), explains cause (15%), data recovery (20%), ownership (20%), next step (20%)

---

## Setup

### Local

```bash
# 1. Clone / unzip the project
cd customer-support-openenv

# 2. Create a virtual environment (Python ≥ 3.10)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the baseline agent
python baseline.py
```

### Docker

```bash
# Build
docker build -t customer-support-openenv .

# Run
docker run --rm customer-support-openenv
```

---

## Usage — Custom Agent

```python
from env import CustomerSupportEnv, Action

env = CustomerSupportEnv()

# Reset to a task
obs = env.reset(difficulty="medium")
print(obs.customer_message)

# Your agent produces an action
action = Action(
    response="I'm sorry for the duplicate charge on order #A8821. "
             "A full refund is being processed now.",
    action_type="refund",
)

# Step through the environment
obs, reward, done = env.step(action)
print(reward.score, reward.passed, reward.feedback)

# Inspect environment state
print(env.state())
```

---

## Environment API

### `CustomerSupportEnv`

| Method | Returns | Description |
|---|---|---|
| `reset(difficulty)` | `Observation` | Start a new episode |
| `step(action)` | `(Observation, Reward, bool)` | Take one action |
| `state()` | `dict` | Current episode metadata |

### Pydantic Models

**`Observation`** — `task_id`, `difficulty`, `customer_message`, `context`, `step`, `done`  
**`Action`** — `response`, `action_type` (`reply` \| `escalate` \| `refund` \| `close`), `metadata`  
**`Reward`** — `score` (0–1), `feedback`, `passed`, `breakdown`

---

## License

MIT