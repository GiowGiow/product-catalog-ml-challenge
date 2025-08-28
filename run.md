# How to Run the Project

This document provides instructions on how to set up and run the product-info-backend service.

## Prerequisites

- Python 3.13
- [uv](https://github.com/astral-sh/uv) (or pip)

## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd product-info-backend
    ```

2. **Create a virtual environment and install dependencies:**
    Using uv:
    ```sh
    uv venv
    uv pip install -e .[dev]
    source .venv/bin/activate
    ```
    Using pip:
    ```sh
    python3.13 -m venv .venv
    source .venv/bin/activate
    pip install -e .[dev]
    ```

## Running the Application

To start the FastAPI server, run the following command:


```sh
uvicorn src.entrypoints.fastapi_app:app --reload
```


The API will be available at `http://127.0.0.1:8000`. You can access the auto-generated documentation at `http://127.0.0.1:8000/docs`.

## Running Tests

To run the test suite, use pytest:

```sh
pytest
```
