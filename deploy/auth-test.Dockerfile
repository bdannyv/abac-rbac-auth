FROM python:3.11.11-slim AS base

# Install OS security updates and cleanup
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Create system group and user first!
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup auth

# Set correct permissions (after user creation)
RUN chown -R auth:appgroup /app

# Install Poetry
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install poetry

# Copy dependency definitions and install them
COPY ./poetry.lock ./pyproject.toml ./alembic.ini ./
RUN poetry install --no-root

# Set Python path environment variable
ENV PYTHONPATH="/app:/app/auth"

# Copy app and test code (use proper chown to avoid permissions issue)
COPY --chown=auth:appgroup ./auth/ ./auth/
COPY --chown=auth:appgroup ./tests/ ./tests/

# Switch to non-root user
USER auth

# Run alembic migrations first, then pytest correctly
CMD ["sh", "-c", "alembic upgrade head && pytest tests"]
