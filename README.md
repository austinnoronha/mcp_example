# MCP Example: Google Trends Scraper

This project is a full-featured Python Celery + Redis server designed to periodically scrape data from Google Trends every 2 hours and save it into daily CSV files. It is structured for maintainability, testing, and production deployment, following best practices for modern Python projects.

## Tech Stack
- **Language:** Python 3.12
- **Task Queue:** Celery
- **Broker:** Redis
- **Database:** Postgres (via Docker Compose)
- **Dependency Management:** Poetry
- **Testing:** pytest, pytest-cov
- **Linting/Formatting:** ruff, isort, ssort
- **Pre-commit Hooks:** pre-commit
- **Containerization:** Docker, Docker Compose

## Project Structure
```
src/
  apis/      # REST endpoints or dashboards
  libs/      # Integration logic (DB, queue consumers)
  models/    # ORM or Pydantic models
  schema/    # Validation schemas
  utils/     # Helpers & utilities
tests/       # All test cases
pyproject.toml
README.md
```

## Getting Started

### 1. Clone the repository
```sh
git clone <repo-url>
cd mcp_example
```

### 2. Set up the virtual environment
```sh
python -m venv .venv
. .venv/Scripts/activate  # On Windows
# or
source .venv/bin/activate  # On Linux/Mac
```

### 3. Install dependencies with Poetry
```sh
pip install poetry
poetry install
```

### 4. Run Docker Compose (for Postgres & Redis)
```sh
docker-compose up -d
```

### 5. Run tests
```sh
poetry run pytest
```

## Common Commands
- **Activate venv:** `. .venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)
- **Install dependencies:** `poetry install`
- **Run tests:** `poetry run pytest`
- **Run linter:** `poetry run ruff src/`
- **Run formatter:** `poetry run isort src/`
- **Run pre-commit hooks:** `poetry run pre-commit run --all-files`
- **Start Docker services:** `docker-compose up -d`

## Contributing
- Use feature branches off `development`.
- PRs should target `staging` for integration, then `main` for production.
- Ensure all tests and linters pass before submitting a PR.

---

For more details, see the documentation in each module. 