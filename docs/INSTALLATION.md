# Zombie Run Cost Killer - Installation Guide

## Prerequisites

1. **Operating System**: Windows 10 / 11 (64-bit)
2. **Python**: Python 3.10+
3. **Node.js**: Node.js 18+ & npm
4. **Docker**: Docker Desktop (for PostgreSQL container)

---

## Step-by-Step Installation

### Step 1: Clone & Navigate to Repository
```powershell
cd c:\Users\ndhee\tripilot
```

### Step 2: Database Setup
Launch PostgreSQL via Docker Compose:
```powershell
docker-compose up -d
```
Verify container is healthy:
```powershell
docker ps
```

### Step 3: Backend Setup
Navigate to `backend/` and create virtual environment:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install backend dependencies:
```powershell
python -m pip install -r requirements.txt
```

Run Alembic database migrations:
```powershell
alembic upgrade head
```

Launch FastAPI development server:
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

### Step 4: Frontend Setup
In a new terminal, navigate to `frontend/`:
```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your web browser.
