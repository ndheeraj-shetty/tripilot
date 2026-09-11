# Zombie Run Cost Killer - Production Deployment & Operations Guide

This guide provides instructions for deploying **Zombie Run Cost Killer** in production environments.

---

## 1. Quick Start with Docker Compose

To launch the full Zombie Run Cost Killer stack (Frontend, FastAPI Backend, and PostgreSQL database):

```bash
docker-compose up --build -d
```

### Access Ports:
- **Frontend Dashboard**: `http://localhost:3000`
- **FastAPI REST API Docs**: `http://localhost:8000/docs`
- **Prometheus Metrics**: `http://localhost:8000/api/v1/admin/metrics`
- **PostgreSQL Database**: `localhost:5432`

---

## 2. Environment Configuration (.env)

Create a `.env` file in the project root directory:

```env
DATABASE_URL=postgresql+asyncpg://trainpilot:trainpilot_secret_pass@localhost:5432/trainpilot_db
SECRET_KEY=your_production_hmac_jwt_secret_key_here
AUTOMATION_DEFAULT_GRACE_PERIOD_SEC=30
GPU_TEMP_CRITICAL_THRESHOLD=85.0
```

---

## 3. Production Health Check & Monitoring Endpoints

- **Live Liveness Probe**: `GET /api/v1/live`
- **Readiness Probe**: `GET /api/v1/ready`
- **Full Health Diagnostics**: `GET /api/v1/health`
- **System Resource Telemetry**: `GET /api/v1/admin/system`
- **Prometheus Text Metrics**: `GET /api/v1/admin/metrics`

---

## 4. Database Backup & Disaster Recovery

Run an on-demand database & workspace snapshot backup:

```bash
curl -X POST http://localhost:8000/api/v1/backup
```

Backups are saved to `./storage/backups/`.
