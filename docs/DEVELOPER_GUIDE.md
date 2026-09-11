# Zombie Run Cost Killer - Developer Guide

## Architectural Philosophy

Zombie Run Cost Killer enforces **Clean Architecture** and **SOLID principles** across both backend and frontend codebases:

1. **Backend Separation of Concerns**:
   - `domain/models`: SQLAlchemy ORM database entities.
   - `domain/schemas`: Pydantic V2 DTOs for strict input validation and response serialization.
   - `repositories`: Pure data access logic isolated from HTTP or business rules.
   - `services`: Business logic, validation, directory creation, and domain orchestrations.
   - `api/v1/endpoints`: Controllers handling HTTP request/response routing and dependency injection.

2. **Frontend Architecture**:
   - `services`: Centralized Axios client (`api.ts`) with global error interceptors.
   - `hooks`: React Query hooks (`useProjects`, `useSettings`) managing server state and cache invalidations.
   - `types`: Single source of truth Zod schemas and inferenced TypeScript interfaces (`projectSchema`).
   - `components`: Reusable layout and notification components.

3. **Logging & Diagnostics**:
   - Structured logging powered by Loguru with console color formatting and 10MB auto-rotating file logs in `backend/logs/zombierun.log`.

---

## Running Tests
To run backend unit tests:
```powershell
cd backend
python -m pytest tests/test_backend.py
```
