# Digital Rule Engine API (Unofficial)

## Overview
The `Digital Rule Engine API` is a scheduled rules engine designed to evaluate and process rules, including campaign flags and other criteria, stored in a local PostgreSQL database. This data is sourced from ADL GAM Datastores and local Data Ponds.

---

## Features
- **Rule Evaluation**: Scheduled evaluation of business rules to manage campaign flags and other conditions.
- **Data Synchronization**: Fetches data from ADL GAM Datastores and integrates with local Data Ponds.
- **Flexible Configuration**: Dynamically configurable using `Pydantic Settings`.
- **Database Management**: Uses SQLAlchemy for ORM and Alembic for database migrations.
- **Robust Testing**: Comprehensive testing suite covering unit, BDD, and integration tests.

---

## Project Dependencies and Tools

### Management Dependencies
- **UV**: Handles dependency management for the project, ensuring consistent environments and compatibility.

### Libraries
- **Formatting**: `Ruff`
- **Linting**: `Pylint`
- **Dependency Management**: `UV`
- **Dynamic Configurations**: `Pydantic Settings`
- **Type Hinting**: `MyPy`
- **Unit Testing**: `Pytest`
- **BDD Testing**: `pytest_bdd`
- **Integration Testing**: `Pytest` and `async_asgi_testclient`
- **Code Scanning**: `Flake8`, `MyPy`, and security-focused scanning tools.
- **Logging**: Built-in `logging` module.
- **Data Handling**: `Pydantic`
- **Database**: `SQLAlchemy`
- **Database Migration**: `Alembic`

---

## Installation

### Prerequisites
1. Python 3.8+
2. Virtual environment support (optional but recommended)
3. [UV](https://uv-mgmt.readthedocs.io/) installed for dependency management.

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/digital-rule-engine-api-unofficial.git
    cd digital-rule-engine-api-unofficial
    ```
2. Set up your environment:
    ```bash
    uv install
    ```
3. Run the application:
    ```bash
    python -m your_main_module
    ```

---

## Configuration
Dynamic configurations are managed via `Pydantic Settings`. Environment-specific configurations can be loaded from `.env` files or other sources.

---

## Testing
This project includes a robust testing suite:

1. **Unit Tests**:
    ```bash
    pytest tests/unit
    ```

2. **BDD Testing**:
    ```bash
    pytest tests/bdd
    ```

3. **Integration Tests**:
    ```bash
    pytest tests/integration
    ```

---

## Code Quality
Maintain code quality with the following tools:

- **Ruff**: Run formatting checks
    ```bash
    ruff .
    ```
- **Pylint**: Perform linting
    ```bash
    pylint your_project_folder
    ```
- **MyPy**: Ensure type hint correctness
    ```bash
    mypy your_project_folder
    ```
- **Flake8**: Scan for additional coding standard violations
    ```bash
    flake8 your_project_folder
    ```

---

## Database Management

- **ORM**: `SQLAlchemy`
- **Migrations**: `Alembic`

### Run Migrations
```bash
alembic upgrade head
```

### Create a New Migration
```bash
alembic revision --autogenerate -m "Migration message"
```

---

## Logging
Logging is managed using Python's built-in `logging` module. Customize logging configurations in the settings file as needed.

---

## Security
Ensure secure code practices with:
- Dependency vulnerability scanning via `UV`.
- Static analysis using `MyPy` and `Flake8`.
- Additional security-focused tools as needed.

---

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit and push your changes.
4. Open a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` file for details.
