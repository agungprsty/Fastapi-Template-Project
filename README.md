# 🚀 FastAPI Clean Architecture with MongoDB

A scalable and production-ready Python backend using **FastAPI**, **Beanie** (MongoDB ODM), and **Domain-Driven Design (DDD)** principles.

---

## 📦 Features

- ⚡ FastAPI — High-performance Python web framework.
- 🍃 Beanie — Asynchronous ODM built on top of Motor & Pydantic v2.
- 🧱 Clean Architecture — Clear separation of domain, infrastructure, and application logic.
- 🔑 JWT Authentication — Ready to extend with RBAC/Scopes.
- 🔄 Lifespan + DI — Dependency Injection and proper async app lifecycle handling.
- 📅 Background Jobs — Ready for APScheduler with MongoDB JobStore.
- 📑 Structured Error Handling — Custom exception classes with unified response format.
- 🧪 Pytest — Testable components and service layer.

---

## 🗂️ Project Structure

### core/
- **`app.py`**: FastAPI app setup, including instance creation and middleware configuration.
- **`di.py`**: Dependency Injection container setup for services and repositories.
- **`error.py`**: Custom exception handler registration for global error management.
- **`lifespan.py`**: Manages lifespan events like database connections on startup and cleanup on shutdown.
- **`routes.py`**: Register and manage all application routes.

### config/
- **`config.py`**: Application settings and environment configuration, often using `.env` files and `pydantic` for validation.

### src/
- **`application/`**: Contains use cases and application logic.
- **`domain/`**: Domain models representing core business logic and entities.
- **`exception/`**: Custom exception classes for specific errors in the application.
- **`infrastructure/`**: Repositories and external adapters for databases, APIs, etc.
- **`routes/`**: API route definitions and controller logic.
- **`utils/`**: Utility functions such as document loaders, parsers, etc.

### log/
- Contains integration logs for the application.

### tests/
- Contains unit and integration tests for the application.

---

## ⚙️ Requirements

- Python >= 3.10
- pip

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/agungprsty/Fastapi-Template-Project.git
cd Fastapi-Template-Project
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment
Rename `.env.example` to `.env` and adjustment according to the needs:

```env
APP_NAME="Fastapi Template Project"
APP_ENV="development"
APP_HOST="127.0.0.1"
APP_PORT=8100
APP_DEBUG=true
```

### 5. Run the application

```bash
python run.py
```

App running in : http://127.0.0.1:8100

## 🧪 Run Tests

```bash
pytest
```

## 📘 API Docs

- Swagger UI: http://127.0.0.1:8100/docs
- ReDoc: http://127.0.0.1:8100/redoc

## 🤝 Contributing
PRs and feedback are very welcome. To contribute:

1. Fork the repo
2. Create a new feature branch
3. Commit changes
4. Submit a pull request

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)  © 2025