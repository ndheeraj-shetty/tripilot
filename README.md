# Zombie Run Cost Killer (V1 Local Edition)

> **AI-Powered ML Training Cost Optimization & Automation Platform**

Zombie Run Cost Killer automates the complete model training lifecycle on a single computer. Unlike traditional passive monitoring tools (such as TensorBoard, MLflow, or Weights & Biases), Zombie Run Cost Killer actively monitors system hardware and training metrics, detects anomalies (Overfitting, Underfitting, NaN loss, GPU overheating, runaway zombie runs), predicts remaining time, and autonomously executes post-training actions (saving best models, generating PDF reports, compressing logs, and triggering computer shutdown/sleep/hibernate).

---

## Phase 1 Foundation Features

- **Backend Architecture**: FastAPI, SQLAlchemy 2.0 Async ORM, Alembic migrations, PostgreSQL, Loguru logger, Pydantic V2 schemas.
- **Clean Architecture Patterns**: Strict separation into Domain Models, Schemas, Repositories, Service Layer, and REST API controllers.
- **Full Project CRUD**: REST APIs and interactive UI for managing ML Projects, framework selection (PyTorch, TensorFlow, Ultralytics YOLO), dataset locations, and script configurations.
- **System Settings Persistence**: System configuration repository and settings management.
- **Frontend Architecture**: React 18, Vite, TypeScript, Tailwind CSS dark theme, React Router v6, Axios, React Query (TanStack Query v5), React Hook Form, Zod validation, Toast notifications.

---

## Quick Start

### 1. Start Infrastructure (PostgreSQL)
```powershell
docker-compose up -d
```

### 2. Backend Setup
```powershell
cd backend
python -m pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload --port 8000
```
- API Health Check: `http://localhost:8000/api/v1/health`
- Swagger API Specs: `http://localhost:8000/docs`

### 3. Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```
- Web Application UI: `http://localhost:3000`

---

## Documentation Links

- [Installation Guide](docs/INSTALLATION.md)
- [Folder Structure Documentation](docs/FOLDER_STRUCTURE.md)
- [REST API Specifications](docs/API_DOCUMENTATION.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
