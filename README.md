## 🚀 Proposed Solution

Here's a breakdown of the technical strategy for this project:

-   **🐍 Programming Language: Python 3.13**
    -   Chosen for its versatility in backend development and being the current Long-Term Support (LTS) version.

-   **🌐 Framework: FastAPI**
    -   Ideal for building APIs quickly and efficiently.
    -   Supports asynchronous programming out of the box.
    -   Provides automatic generation of OpenAPI documentation.

-   **💾 Data Persistence**
    -   **Repository Pattern:** An abstraction layer for data access.
    -   **Caching:** In-memory caching for improved performance.
    -   **Storage:** Custom JSON/CSV file-based storage.

-   **☁️ Deployment**
    -   **Containerization:** Docker.
    -   **Orchestration:** Kubernetes.

-   **⚙️ CI/CD**
    -   **Pipeline:** GitHub Actions.
    -   **Code Quality:** Pre-commit hooks to lint, format, and scan for vulnerabilities before committing.
    -   **Merge Checks:** Runs for each pull request against `development` and `main` branches.
    -   **Test Coverage:** Minimum 80% coverage required to merge.

-   **🌳 Git Workflow**
    -   **Branches:**
        -   `main`: Production-ready code.
        -   `development`: Latest development changes.
        -   `feature/*`: For new features or bug fixes.
    -   **Merging:**
        -   Pull Requests are required to merge code into `development` and `main`.
        -   PRs must have at least one approval and pass all CI checks.

-   **✨ Code Quality & Linting**
    -   **Pre-commit:** For running automated checks before commits.
    -   **Ruff:** For high-performance linting and formatting.
    -   **Bandit:** For vulnerability scanning.

-   **🧪 Testing**
    -   **Framework:** `pytest` for unit and integration tests.
    -   **Methodology:** Test-Driven Development (TDD) combined with Behavior-Driven Development (BDD).

-   **📖 Documentation & BDD**
    -   **API Docs:** Served automatically via FastAPI's built-in OpenAPI support.
    -   **BDD with `pytest-bdd`:**
        -   Feature files act as a development roadmap.
        -   Serves as living documentation for developers.
        -   Works well with GenAI tools for faster development cycles.

-   **📦 Dependency Management**
    -   **UV:** For managing dependencies, virtual environments, and Python versions.

-   **🏗️ Modeling**
    -   **Domain-Driven Design (DDD):** Following Cosmic Python guidelines for a clear separation of concerns, making the application easier to maintain and scale.

-   **🤖 GenAI Tools**
    -   **GitHub Copilot:** For code suggestions and autocompletion.
    -   **Gemini:** For brainstorming, code suggestions, and design patterns.

## 🤔 Why This Architecture?

The architecture is designed to be **modular, scalable, and maintainable**, following the principles of **Onion Architecture** to ensure loose coupling and high cohesion.

![Onion Model](docs/content/onion_model.png)

The core domain logic sits at the center, independent of external frameworks or infrastructure. Dependencies point inwards, preventing the core business logic from being coupled to implementation details like databases or web frameworks.

![Coupling Diagram](docs/content/coupling.png)

-   **Separation of Concerns:** The service layer (business logic) is distinctly separated from entrypoints (FastAPI) and infrastructure (data persistence).
-   **Repository Pattern:** We use a repository pattern to abstract the data access layer. This allows for easily swapping storage mechanisms (e.g., from in-memory to a database) without impacting business logic.
-   **Unit of Work Pattern:** Manages transactions to ensure data consistency across multiple operations, which is crucial for supporting parallel replicas behind a load balancer.
-   **Behavior-Driven Design (BDD):** We use Gherkin syntax in `.feature` files to drive development. This human-readable format ensures the implementation aligns with requirements and helps new developers understand system behavior quickly.
-   **Automation:** The use of pre-commit hooks and CI/CD pipelines ensures high code quality is maintained throughout the development lifecycle.
-   **Functionality:** The service provides full CRUD operations for the Product model, secured with simple token-based authentication.

## 💡 Why This Stack?

I intentionally chose a production-grade stack not because the problem's complexity demanded it, but to demonstrate proficiency with the tools and practices used to build scalable, maintainable, and robust systems like those at Mercado Libre.