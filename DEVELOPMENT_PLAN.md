### Proposed Solution

Current Strategy:

- Python 3.13:
    - As I currently use Python for most of my projects and it is a versatile language for backend development.
    - Current LTS version.

- Framework:
    - Django:
        - great for rapid development and has a large ecosystem.
        - great for prototyping ideas quickly.
        - currently the framework I am most familiar with.

- Data Persistence Layer:
    - Custom Django Database Backend:
        - To meet the requirement of not using real databases and persisting everything in local JSON or CSV files.
        - Implement a custom database backend that reads from and writes to JSON/CSV files.
        - This backend will handle CRUD operations by manipulating the file directly.
        - For read operations, it will load the entire file into memory for quick access.
        - For write operations, it will update the in-memory data and then write back to the file.
        - This approach ensures that we can leverage Django's ORM capabilities while adhering to the challenge constraints.
        - The custom backend will be designed to handle concurrent access and ensure data integrity.

- Deployment:
    - Docker for containerization
    - Kubernetes for orchestration

- CI/CD:
    - Github CI/CD:
    - Code Quality checks:
        - use pre-commit hooks (to simplify the process of maintaining code quality)
        - Runs for each MR/RP for the development and main branches
    - Coverage checks:
        - Minimum 80% coverage required to merge a PR

- Git Workflow:
    - Branches:
        - main for production-ready code
        - development for the latest development changes
        - feature branches based on development for new features or bug fixes
    - Merging:
        - PRs/MRs to merge feature branches into development
        - PRs/MRs to merge development into main
        - All PRs/MRs require at least one approval and successful CI/CD checks
- Code Quality:
    - Pre-commit for pre-commit hooks to ensure code quality
        - ruff for linting and formatting
        - Bandit for vulnerability scanning
        - mypy for static type checking

- Testing:
    - pytest for unit and integration tests
    - TDD with BDD for behavior-driven development

- Linting:
    - ruff for code quality and consistency

- Documentation:
    - Sphinx for generating project documentation
    - Serves sphinx as an artifact in the CI/CD pipeline for easy access

- Documentation/Testing:
    - BDD development with pytest-bdd
        - Serves as roadmap for development
        - Serves as documentation for other developers
        - Works really well with GenAI tools
            - General framework for the feature as guideline
            - Faster diagrams with MermaidJS

- Diagrams:
    - MermaidJS for diagrams based on the feature files

- Dependency Management:
    - UV for managing dependencies, virtual environments, and python versions

- Modeling:
    - DDD for domain-driven design (mostly using Cosmic Python guidelines)
        - clear separation of concerns
        - easier to maintain and scale the application

- GenAI Tools:
    - Copilot:
        - for code suggestions and autocompletion
    - Gemini:
        - for code suggestions, design suggestions and for brainstorming

### Why This Stack?".
I intentionally chose a production-grade stack not because the problem's complexity demanded it, but to demonstrate your proficiency with the tools and practices used to build scalable, maintainable, and robust systems like those at Mercado Libre.


# Development Plan & Project Structure

This document outlines the development plan, project structure, and key milestones for building the backend API for an item detail page, as per the task challenge.

## 1. Philosophy & Approach

Our approach is to build a robust, scalable, and maintainable API by applying production-grade practices from the outset. We will use Domain-Driven Design (DDD) to model the business logic clearly and Test-Driven Development (TDD) with BDD to ensure our implementation is correct and serves as living documentation. The entire development lifecycle will be automated through a CI/CD pipeline to maintain high code quality and streamline deployments.

## 2. Development Phases & Milestones

### Phase 1: Project Scaffolding & CI/CD Setup (Day 1-2)

The goal of this phase is to establish a solid foundation for the project with all the necessary tooling and automation in place.

**Task 1: Initialize Project Repository**
- Create a new Git repository.
- Initialize README.md, run.md, and prompts.md.
- Set up main and development branches.
- Configure branch protection rules for main and development.

**Task 2: Setup Python Environment with uv**
- Initialize a pyproject.toml file.
- Install initial dependencies: django, djangorestframework, pytest, pytest-bdd, ruff, bandit, mypy, pre-commit, sphinx.

**Task 3: Django Project & App Setup**
- Create the Django project (mercadolibre_api) inside a src directory.
- Create the core application (catalog) inside the src directory.
- Configure settings.py for the project.

**Task 4: Configure Code Quality Tools**
- Initialize pre-commit with hooks for ruff (linting/formatting), bandit (security), and mypy (type checking).
- Configure ruff and mypy settings in pyproject.toml.

**Task 5: Setup CI/CD Pipeline (GitHub Actions)**
- Create a workflow file (.github/workflows/ci.yml).
- Define jobs for:
  - Linting and formatting checks (ruff).
  - Security scanning (bandit).
  - Running tests (pytest).
  - Checking test coverage (minimum 80%).
- Trigger the workflow on pull requests to development and main.

**Task 6: Documentation Setup with Sphinx**
- Initialize Sphinx in a docs/ directory.
- Configure conf.py to use autodoc and apidoc to generate documentation from docstrings.
- Add a CI/CD step to build and deploy documentation as an artifact.

### Phase 2: Core Domain & Custom Data Persistence (Day 3-4)

This phase focuses on modeling the core domain and implementing the custom persistence layer to handle JSON/CSV files as required.

**Task 1: Define the Domain Model (DDD)**
- Identify entities, value objects, and aggregates for the catalog domain.
  - Entity: Product (with attributes like id, title, price, currency, description, images).
  - Value Object: Price (amount, currency).
- Create initial data models in src/catalog/domain/models.py.

**Task 2: Implement Custom Database Backend**
- Create a new Django app for the custom backend (e.g., json_db_backend) inside src.
- Implement the custom database backend logic to read from a products.json file.
- Focus on read operations first to get data flowing.
- Configure Django's DATABASES setting to use this custom backend.

**Task 3: Create Initial BDD Feature File**
- Create src/catalog/tests/features/get_product_details.feature.
- Write scenarios in Gherkin syntax for fetching a product by its ID (happy path and error cases like "product not found").

**Task 4: Implement the API Endpoint (TDD)**
- Write pytest tests for the API view based on the feature file.
- Create the Django Rest Framework Serializer for the Product entity.
- Create the API ViewSet to handle the /api/items/<item_id>/ endpoint.
- Implement the service layer logic to fetch data from the repository (which uses the custom DB backend).
- Ensure all tests pass.

### Phase 3: Refinement, Error Handling & Containerization (Day 5)

With a working endpoint, this phase is about making the solution more robust and ready for submission.

**Task 1: Enhance Error Handling**
- Implement custom exception handling in Django Rest Framework to provide clear, structured error responses (e.g., 404 Not Found, 400 Bad Request).
- Add BDD scenarios for different error conditions.

**Task 2: Dockerize the Application**
- Create a Dockerfile for the Django application.
- Create a docker-compose.yml for easy local development and testing.

**Task 3: Finalize Documentation**
- Update README.md with final API design explanation, setup instructions, and architectural decisions.
- Ensure run.md has clear instructions on how to run the project using Docker.
- Populate prompts.md with examples of prompts used with GenAI tools.
- Ensure all code has clear docstrings for Sphinx to generate the documentation.

**Task 4: Final Review and Submission**
- Review all requirements.
- Run all checks and tests one last time.
- Zip the project folder for submission.

## 3. Project Structure (DDD-inspired)

Here is the proposed directory structure that separates concerns according to DDD principles.

```
mercadolibre-api/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD pipeline
├── .vscode/                   # VSCode settings (optional)
├── data/
│   └── products.json          # The "database" file
├── docs/                      # Sphinx documentation source
│   ├── source/
│   │   ├── conf.py
│   │   └── index.rst
├── src/                       # Source code directory
│   ├── catalog/               # Core domain app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── domain/            # Domain layer (pure Python, no framework)
│   │   │   ├── __init__.py
│   │   │   ├── models.py      # Domain entities and value objects
│   │   │   └── repositories.py# Abstract repository interfaces
│   │   ├── infrastructure/    # Infrastructure layer (framework-specific)
│   │   │   ├── __init__.py
│   │   │   └── repositories.py# Concrete repository implementations
│   │   ├── service_layer/     # Application service layer
│   │   │   ├── __init__.py
│   │   │   └── services.py    # Business logic and use cases
│   │   ├── entrypoints/       # API layer (Django Rest Framework)
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   └── views.py
│   │   ├── tests/
│   │   │   ├── features/
│   │   │   │   └── get_product_details.feature
│   │   │   └── step_definitions/
│   │   │       └── test_get_product_details.py
│   │   └── urls.py
│   ├── json_db_backend/       # Custom DB backend app
│   │   └── ...
│   └── mercadolibre_api/      # Django project root
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pyproject.toml             # Project metadata and tool config (uv, ruff, mypy)
├── README.md
├── run.md
└── prompts.md
```

This structure clearly separates the core domain logic from the framework-specific implementation details, making the application easier to test, maintain, and evolve.