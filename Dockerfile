# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Metadata ──────────────────────────────────────────────────────────────────
LABEL maintainer="your-name"
LABEL description="Customer Support OpenEnv baseline runner"

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Dependencies ──────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Source code ───────────────────────────────────────────────────────────────
COPY . .

# ── Run baseline agent ────────────────────────────────────────────────────────
CMD ["python", "baseline.py"]