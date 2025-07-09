"""
main.py
-------
FastAPI application for MCP server: generates custom project prompts via Celery tasks.

## Example request for /generate-prompt/
{
  "objective": "Create a FastAPI app with Celery to show messages shared by different users",
  "tech_stack": "Python 3.12, Celery, Redis, Git, Pytest",
  "git_tool": "github",
  "user_info": "Austin Noronha"
}
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.libs.prompt import generate_prompt_task, celery_app
from src.utils.helpers import get_logger
from src.utils.config import REDIS_URL
from fastapi.responses import JSONResponse
from typing import Optional
import redis

logger = get_logger(__name__)

app = FastAPI(
    title="MCP Prompt Generator API",
    description="API for generating custom project prompts using Celery and FastAPI.",
    version="1.0.0"
)

class PromptRequest(BaseModel):
    # The PromptRequest model defines the expected request body for the /generate-prompt/ endpoint.
    # Fields:
    #   - objective: The main goal or objective for the project.
    #   - tech_stack: The technology stack to be used.
    #   - git_tool: The Git tool or platform (e.g., GitHub, GitLab).
    #   - user_info: Information about the user requesting the prompt.
    #
    objective: str
    tech_stack: str
    git_tool: str
    user_info: str

class MetadataResponse(BaseModel):
    name: str
    description: str
    version: str
    capabilities: list[str]
    maintainer: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    detail: Optional[str] = None

async def generate_prompt(req: PromptRequest):
    """
    Initiates a Celery task to generate a custom project prompt.

    Args:
        req (PromptRequest): The request body containing:
            - objective (str): The main goal or objective for the project.
            - tech_stack (str): The technology stack to be used.
            - git_tool (str): The Git tool or platform (e.g., GitHub, GitLab).
            - user_info (str): Information about the user requesting the prompt.

    Returns:
        dict: A dictionary containing:
            - task_id (str): The unique identifier for the Celery task.
            - status (str): The status of the task initiation ("processing").

    Raises:
        HTTPException: If the Celery task fails to start, returns a 500 error.
        
    Example:
    {
        "objective": "Create a FastAPI app with Celery to show messages shared by different users",
        "tech_stack": "Python 3.12, Celery, Redis, Git, Pytest",
        "git_tool": "github",
        "user_info": "Austin"
    }
    """
    logger.info(f"Received prompt generation request: {req}")
    try:
        task = generate_prompt_task.delay(req.objective, req.tech_stack, req.git_tool, req.user_info)
        logger.info(f"Prompt generation task started with ID: {task.id}")
        return {"task_id": task.id, "status": "processing"}
    except Exception as e:
        logger.error(f"Failed to start prompt generation task: {e}")
        raise HTTPException(status_code=500, detail="Failed to start prompt generation task.")

# MCP-compliant inference endpoint (alias)
@app.post("/v1/infer", summary="MCP inference endpoint", response_description="Task ID and status")
async def mcp_infer(req: PromptRequest):
    return await generate_prompt(req)

@app.get("/task-status/{task_id}", summary="Get status/result of a prompt generation task", response_description="Task status and result if available")
async def get_task_status(task_id: str):
    logger.info(f"Checking status for task ID: {task_id}")
    try:
        result = celery_app.AsyncResult(task_id)
        if result.state == "PENDING":
            logger.info(f"Task {task_id} is pending.")
            return {"status": "pending"}
        elif result.state == "SUCCESS":
            logger.info(f"Task {task_id} completed successfully.")
            return {"status": "success", "result": result.result}
        elif result.state == "FAILURE":
            logger.error(f"Task {task_id} failed: {result.info}")
            return {"status": "failure", "error": str(result.info)}
        else:
            logger.info(f"Task {task_id} is in state: {result.state}")
            return {"status": result.state.lower()}
    except Exception as e:
        logger.error(f"Error checking status for task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to check task status.")

@app.get("/v1/metadata", response_model=MetadataResponse, summary="MCP metadata endpoint")
async def get_metadata():
    return MetadataResponse(
        name="MCP Prompt Generator API",
        description="API for generating custom project prompts using Celery and FastAPI.",
        version="1.0.0",
        capabilities=["prompt-generation", "async-tasks"],
        maintainer="Austin Noronha"
    )

@app.get("/v1/health", response_model=HealthResponse, summary="MCP health check endpoint")
async def get_health():
    redis_ok = False
    celery_ok = False
    details = []
    # Check Redis
    try:
        r = redis.Redis.from_url(REDIS_URL)
        if r.ping():
            redis_ok = True
        else:
            details.append("Redis ping failed")
    except Exception as e:
        details.append(f"Redis error: {e}")
    # Check Celery
    try:
        ping_result = celery_app.control.ping(timeout=1.0)
        if ping_result and isinstance(ping_result, list) and len(ping_result) > 0:
            celery_ok = True
        else:
            details.append("No Celery workers responded to ping")
    except Exception as e:
        details.append(f"Celery error: {e}")
    # Compose status
    if redis_ok and celery_ok:
        return HealthResponse(status="ok")
    else:
        return HealthResponse(status="degraded", detail=", ".join(details)) 