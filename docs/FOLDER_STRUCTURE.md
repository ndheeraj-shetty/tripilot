# Zombie Run Cost Killer - Folder Structure Documentation

```
tripilot/
├── docker-compose.yml              # PostgreSQL Docker database setup
├── README.md                       # Main project overview & quick start
├── docs/                           # Enterprise documentation suite
│   ├── INSTALLATION.md             # Installation & environment guide
│   ├── FOLDER_STRUCTURE.md         # Folder architecture specification
│   ├── API_DOCUMENTATION.md        # REST API endpoint reference
│   └── DEVELOPER_GUIDE.md          # Engineering standards & guidelines
├── backend/                        # FastAPI Python Core
│   ├── alembic.ini                 # Alembic migration configuration
│   ├── requirements.txt            # Python dependencies
│   ├── alembic/                    # Database migration scripts
│   │   ├── env.py
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   ├── app/
│   │   ├── main.py                 # FastAPI application entrypoint
│   │   ├── api/                    # REST API routes & controllers
│   │   │   └── v1/
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── health.py   # GET /health
│   │   │           ├── projects.py # GET, POST, PUT, DELETE /projects
│   │   │           └── settings.py # GET, PUT /settings
│   │   ├── core/                   # Infrastructure configuration
│   │   │   ├── config.py           # Pydantic Settings & env configuration
│   │   │   ├── database.py         # SQLAlchemy 2.0 Async Sessionmaker
│   │   │   └── logging_config.py   # Loguru logging setup
│   │   ├── domain/                 # Domain entities & validation DTOs
│   │   │   ├── models/             # SQLAlchemy ORM Data Models
│   │   │   │   └── models.py       # Project, Configuration, TrainingSession
│   │   │   └── schemas/            # Pydantic Request/Response Schemas
│   │   │       └── project_schema.py
│   │   ├── repositories/           # Data Access Layer (Repository Pattern)
│   │   │   ├── project_repo.py
│   │   │   └── config_repo.py
│   │   └── services/               # Business Logic Layer (Service Pattern)
│   │       ├── project_service.py
│   │       └── settings_service.py
│   └── tests/                      # Pytest suite
│       └── test_backend.py
└── frontend/                       # React 18 + Vite + TypeScript Frontend
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── main.tsx
        ├── App.tsx                 # Router & TanStack Query Provider
        ├── index.css               # Tailwind CSS & glassmorphic styling
        ├── components/
        │   ├── common/
        │   │   └── Toast.tsx       # Toast notifications provider & hook
        │   └── layout/
        │       ├── Layout.tsx      # App Layout wrapper
        │       ├── Navbar.tsx      # Top Navigation bar
        │       ├── Sidebar.tsx     # Navigation sidebar
        │       └── Footer.tsx      # Footer
        ├── hooks/
        │   ├── useProjects.ts      # React Query hooks for Project CRUD
        │   └── useSettings.ts      # React Query hook for Settings
        ├── pages/
        │   ├── DashboardPage.tsx   # Dashboard cards overview
        │   ├── ProjectsPage.tsx    # Project CRUD with Zod validation
        │   ├── SettingsPage.tsx    # App Settings & DB configuration
        │   ├── TrainingPage.tsx    # Live Training placeholder
        │   ├── AnalyticsPage.tsx   # Analytics placeholder
        │   ├── AutomationPage.tsx  # Automation placeholder
        │   ├── ReportsPage.tsx     # Reports placeholder
        │   └── AboutPage.tsx       # Platform overview
        ├── services/
        │   ├── api.ts              # Axios instance & error interceptor
        │   ├── projectsApi.ts      # Projects API calls
        │   └── settingsApi.ts      # Settings API calls
        └── types/
            └── project.ts          # Zod schemas & TypeScript types
```
