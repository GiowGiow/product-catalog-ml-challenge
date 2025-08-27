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
