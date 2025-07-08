from celery import Celery
from src.utils.config import REDIS_URL
celery_app = Celery(
    'prompt',
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task
def generate_prompt_task(objective, tech_stack, git_tool, user_info):
    # Compose the prompt here
    prompt = (
        f"Objective: {objective}\n"
        f"Tech Stack: {tech_stack}\n"
        f"Git Tool: {git_tool}\n"
        f"User Info: {user_info}\n"
        "Please generate a project starter prompt with best practices."
    )
    return prompt
