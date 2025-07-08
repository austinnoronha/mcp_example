# MCP Prompt Generator

A Minimal Control Plane (MCP) server for generating custom, pre-formatted prompts to help users start new software projects. This app provides a FastAPI-based API and uses Celery with Redis for asynchronous prompt generation tasks.

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
project-root/
├── src/
│   ├── apis/        # FastAPI endpoints
│   │   └── main.py
│   ├── libs/        # Core logic (prompt generation, Celery tasks)
│   │   └── prompt.py
│   ├── utils/       # Helpers & config
│   │   ├── config.py
│   │   └── helpers.py
├── tests/           # Test cases
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
```

## Example Prompt Request
```
POST /generate-prompt/
{
  "objective": "Create a FastAPI app with Celery to show messages shared by different users",
  "tech_stack": "Python 3.12, Celery, Redis, Git, Pytest",
  "git_tool": "github",
  "user_info": "Austin"
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

## Common Commands
- **Run tests:** `poetry run pytest`
- **Run linter:** `poetry run ruff src/`
- **Run formatter:** `poetry run isort src/`
- **Run pre-commit hooks:** `poetry run pre-commit run --all-files`

## Contributing
- Use feature branches off `development`.
- PRs should target `staging` for integration, then `main` for production.
- Ensure all tests and linters pass before submitting a PR.

---
For more details, see the documentation in each module. 