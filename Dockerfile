# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependency files to the working directory
COPY pyproject.toml uv.lock ./

# Install uv, the package manager
RUN pip install uv

# Install dependencies
RUN uv pip install --system -e .[dev]

# Copy the rest of the application code to the working directory
COPY . .

# Command to run the application
CMD ["uvicorn", "src.entrypoints.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
