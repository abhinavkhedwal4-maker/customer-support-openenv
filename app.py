import gradio as gr
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


def run_task(difficulty: str, custom_response: str, action_type: str):
    obs = env.reset(difficulty=difficulty)
    response_text = custom_response.strip() if custom_response.strip() else BASELINE_RESPONSES[difficulty].response
    action = Action(response=response_text, action_type=action_type)
    _, reward, _ = env.step(action)

    breakdown_text = "\n".join(f"  {k}: {v}" for k, v in reward.breakdown.items())
    result = f"""
📋 TASK: {obs.task_id}  |  Difficulty: {difficulty.upper()}
👤 Customer: {obs.customer_message}

🤖 Agent Response: {response_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SCORE:    {reward.score:.3f} / 1.000
✅ PASSED:   {reward.passed}
💬 FEEDBACK: {reward.feedback}

📈 BREAKDOWN:
{breakdown_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return result


with gr.Blocks(title="Customer Support OpenEnv") as demo:
    gr.Markdown("# 🎧 Customer Support OpenEnv")
    gr.Markdown("An OpenEnv-style RL environment for customer support tasks. Test your agent responses below.")

    with gr.Row():
        difficulty = gr.Dropdown(
            ["easy", "medium", "hard"],
            value="easy",
            label="Task Difficulty"
        )
        action_type = gr.Dropdown(
            ["reply", "refund", "escalate", "close"],
            value="reply",
            label="Action Type"
        )

    custom_response = gr.Textbox(
        label="Agent Response (leave blank to use baseline)",
        placeholder="Type a custom agent response here, or leave blank for baseline...",
        lines=4,
    )

    run_btn = gr.Button("▶ Run Task", variant="primary")
    output = gr.Textbox(label="Results", lines=18)

    run_btn.click(
        fn=run_task,
        inputs=[difficulty, custom_response, action_type],
        outputs=output
    )

    gr.Markdown("### 🚀 Baseline Scores")
    gr.Markdown("""
| Task   | Score | Passed |
|--------|-------|--------|
| Easy   | 1.000 | ✅     |
| Medium | 1.000 | ✅     |
| Hard   | 1.000 | ✅     |
""")

demo.launch(server_name="0.0.0.0", server_port=7860)