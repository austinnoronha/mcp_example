# MCP Prompt Generator

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/your-repo/actions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-Swagger%20UI-blue)](http://localhost:8000/docs)

A Minimal Control Plane (MCP) server for generating custom, pre-formatted prompts to help users start new software projects. This app provides a FastAPI-based API and uses Celery with Redis for asynchronous prompt generation tasks.

---

## MCP Protocol Reference
This service is compatible with the [Model Collaboration Protocol (MCP)](https://github.com/model-collaboration-protocol/spec). MCP is a standard for interoperable AI and automation services. See the [specification](https://github.com/model-collaboration-protocol/spec) for details on endpoints and schemas.

## Objective
- Collect user requirements (objective, tech stack, git tool, user info).
- Generate a tailored project prompt for LLMs (Claude, ChatGPT, etc.) using best practices.
- Provide an API for submitting prompt requests and checking their status.

## What is MCP?
**MCP (Minimal Control Plane)** is a lightweight, modular backend service that orchestrates and automates developer workflows. In this example, MCP acts as a prompt-generation engine, providing a simple API and logic to help users kickstart new projects with clear, actionable instructions.

## Technologies Used
- **Python 3.12**
- **FastAPI** (REST API)
- **Celery** (Task queue)
- **Redis** (Broker & result backend)
- **Poetry** (Dependency management)
- **Docker & Docker Compose** (Containerization)
- **pytest, ruff, isort, ssort, pre-commit** (Dev tools)

## Folder Structure
```
mcp_example/
├── src/
│   ├── apis/
│   │   └── main.py           # FastAPI app and API endpoints
│   ├── libs/
│   │   ├── prompt.py         # Celery app and prompt generation task
│   │   └── openrouter.py     # Model interaction logic
│   ├── utils/
│   │   ├── config.py         # Configuration (env, Redis URL, etc.)
│   │   └── helpers.py        # Logging and utility functions
├── test_e2e_openrouter.py    # End-to-end test for OpenRouter
├── tests/                    # Additional tests
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
```

## Example Prompt Request
```
# Request
POST /v1/infer
- Payload
{
  "objective": "Create a FastAPI app with Celery to show messages shared by different users",
  "tech_stack": "Python 3.12, Celery, Redis, Git, Pytest",
  "git_tool": "github",
  "user_info": "Austin"
}

# Response
{
  "task_id": "822e05c6-2a45-4146-98e5-1dc953372824",
  "status": "processing"
}

# Request
GET /v1/task-status/{task_id}
- Payload
822e05c6-2a45-4146-98e5-1dc953372824

# Response
{
  "status": "success",
  "result": [
    "You are an expert project assistant. Build my project with best coding practices.\nMy Project Information and Context on Technology: \nObjective: Create a FastAPI app with Celery to show messages shared by different users\nTech Stack: Python 3.12, Celery, Redis, Git, Pytest\nGit Tool: github\nUser Info: Austin\nFolder structure modular design: \n├── app/ \n│   ├── core/               # Configs, utils, security \n│   ├── api/                # FastAPI routes \n│   ├── models/             # Pydantic/SQLAlchemy models \n│   ├── tasks/              # Celery tasks \n│   └── main.py             # FastAPI app entrypoint \n├── tests/                  # Pytest tests (API, tasks, etc.) \n├── .env                   # Environment variables \n├── requirements.txt       # Dependencies \n├── docker-compose.yml     # Redis + App + Worker setup (optional) \n└── README.md              # Setup Readme with basic information about the project \nStart by creating the our project.toml file. (if not present) \n Run the cmd on the terminal to intialize it.\nNext create venv and poetry with its.\nNext please create the folder strcuture and files. Try to create __init__.py file.\nNote: when I ask to create code/function/class try to use best industry standards \n",
    "of that technology specified and add enough documentation to the respective file/function/code.\n"
  ]
}
```

## Usage

### 1. Clone the repository
```sh
git clone <repo-url>
cd mcp_example
```

### 2. Install dependencies (with Poetry)
```sh
python -m venv .venv
. .venv/Scripts/activate  # On Windows
# or
source .venv/bin/activate  # On Linux/Mac
pip install poetry
poetry install
```

### 3. Start Redis (if not using Docker Compose)
```sh
# On Linux/Mac
redis-server
# On Windows, use Docker or Redis installer
```

### 4. Start the FastAPI app (standalone)
```sh
poetry run uvicorn src.apis.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start the Celery worker (standalone)
```sh
poetry run celery -A src.libs.prompt.celery_app worker --loglevel=info --pool=solo
```

### 6. Or use Docker Compose (recommended)
```sh
docker-compose up --build
```
- API available at: http://localhost:8000
- Celery worker and Redis run in containers

### 7. API Documentation
- Visit http://localhost:8000/docs for interactive Swagger UI

## API Signatures

### 1. `POST /generate-prompt/`
- **Request:**
  ```json
  {
    "objective": "Create a FastAPI app with Celery to show messages shared by different users",
    "tech_stack": "Python 3.12, Celery, Redis, Git, Pytest",
    "git_tool": "github",
    "user_info": "Austin"
  }
  ```
- **Response:**
  ```json
  { "task_id": "<celery-task-id>", "status": "processing" }
  ```

### 2. `POST /v1/infer`
- **Request:** (same as `/generate-prompt/`)
- **Response:** (same as `/generate-prompt/`)

### 3. `GET /task-status/{task_id}`
- **Response (pending):**
  ```json
  { "status": "pending" }
  ```
- **Response (success):**
  ```json
  { "status": "success", "result": "<prompt-result>" }
  ```
- **Response (failure):**
  ```json
  { "status": "failure", "error": "<error-message>" }
  ```

### 4. `GET /v1/metadata`
- **Response:**
  ```json
  {
    "name": "MCP Prompt Generator API",
    "description": "API for generating custom project prompts using Celery and FastAPI.",
    "version": "1.0.0",
    "capabilities": ["prompt-generation", "async-tasks"],
    "maintainer": "Austin Noronha"
  }
  ```

### 5. `GET /v1/health`
- **Response (healthy):**
  ```json
  { "status": "ok" }
  ```
- **Response (degraded):**
  ```json
  { "status": "degraded", "detail": "Redis error: ... , No Celery workers responded to ping" }
  ```

## Usage Tips

Here are some quick examples for using the API with `curl`:

- **Check service metadata:**
  ```sh
  curl http://localhost:8000/v1/metadata
  ```
- **Check health:**
  ```sh
  curl http://localhost:8000/v1/health
  ```
- **Submit a prompt generation request:**
  ```sh
  curl -X POST http://localhost:8000/v1/infer \
    -H "Content-Type: application/json" \
    -d '{
      "objective": "Create a FastAPI app with Celery to show messages shared by different users",
      "tech_stack": "Python 3.12, Celery, Redis, Git, Pytest",
      "git_tool": "github",
      "user_info": "Austin"
    }'
  ```
- **Check task status:**
  ```sh
  curl http://localhost:8000/task-status/<task_id>
  ```

## Common Commands
- **Run tests:** `poetry run pytest`
- **Run linter:** `poetry run ruff src/`
- **Run formatter:** `poetry run isort src/`
- **Run pre-commit hooks:** `poetry run pre-commit run --all-files`

## Contributing
- Use feature branches off `development`.
- PRs should target `staging` for integration, then `main` for production.
- Ensure all tests and linters pass before submitting a PR.

## New APIs

Planned or recently added endpoints:
- `/v1/completions` (future): Standardized completions endpoint for broader MCP compatibility.
- `/v1/capabilities` (future): Returns supported features and models.
- `/v1/metrics` (future): Service usage and health metrics.

_Contributions and suggestions for new APIs are welcome!_

---
For more details, see the documentation in each module. 