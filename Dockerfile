# 1. Base stage: Use a pre-built image with Python and uv.
# This stage is for installing dependencies.
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set cache directory for uv
ENV UV_CACHE_DIR=/tmp/uv-cache

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment, using a cache mount for speed.
# This creates a self-contained .venv directory.
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    uv sync --locked

# Copy the rest of the application code
COPY . .

# Install the project itself into the virtual environment
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    uv pip install --no-deps --editable .

# 2. Development stage: Use the builder environment.
# The CMD will run the app with hot-reloading.
FROM builder as development

CMD ["uv", "run", "uvicorn", "src.entrypoints.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# 3. Production stage: Create a slim final image.
# Start from a clean python image.
FROM python:3.13-slim as production

ENV APP_MODE=production
# Set work directory
WORKDIR /app

# Create a non-root user
RUN addgroup --system nonroot && adduser --system --ingroup nonroot nonroot
USER nonroot

# Copy only the virtual environment from the builder stage.
# This keeps the image small and secure.
COPY --from=builder --chown=nonroot:nonroot /app/.venv ./.venv
COPY --from=builder --chown=nonroot:nonroot /app/src ./src

# Set the PATH to include the venv
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the application in production mode
CMD ["uvicorn", "src.entrypoints.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
