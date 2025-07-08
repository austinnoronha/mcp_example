# Use official Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy poetry 
COPY pyproject.toml poetry.lock ./

RUN pip install poetry==1.8.3 && poetry install --only main --no-root --no-directory

COPY src/ ./src/

# Set default command (optional; overridden in docker-compose.yml)
CMD ["uvicorn", "src.apis.main:app", "--host", "0.0.0.0", "--port", "8000"]
