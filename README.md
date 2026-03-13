# FIO API

> "The AI acts as an advisor only — every suggestion must pass automated policy rules and a structured approval process before it triggers any real action."

Fio is an autonomous finance agent API built for teams that need AI-assisted financial workflows without sacrificing safety or auditability. It handles financial task management with a planned AI layer that advises but never executes directly.

Built with Python, FastAPI, PostgreSQL, SQLAlchemy, and Alembic.

---

## Local Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- pip

### 1. Clone the repo
```bash
git clone https://github.com/your-username/fio-api.git
cd fio-api
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
Copy the example env file and fill in your values:
```bash
cp .env.example .env
```

Required variables:
```
PROJECT_NAME="Fio API"
ENVIRONMENT="development"        # development, staging, production
DEBUG="true"
DATABASE_URL=""                  # Runtime user - used by the running application
MIGRATION_DATABASE_URL=""        # Migration user - only used for migrations
ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8000"
```

### 4. Set up the database
Run the scripts in order under the correct user. Scripts are found in `backend/app/scripts/`.

1. Connect to `fioapi_db` as `postgres` → run `db_setup01_postgres.sql`
2. Connect to `fioapi_db` as `fioapi_admin` → run `db_setup02_fioapi_admin.sql`

### 5. Run migrations
```bash
alembic upgrade head
```

### 6. Start the server
```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Returns app status and current environment |
| `POST` | `/tasks/` | Create a new task |
| `GET` | `/tasks/{task_id}` | Fetch a task by ID |
| `GET` | `/tasks/` | List tasks (paginated, 1000 max) |
| `PUT` | `/tasks/{task_id}` | Update a task by ID |
| `DELETE` | `/tasks/{task_id}` | Delete a task by ID |

---

## Architecture

> **Note:** Fio is under active development. The sections below reflect both what is currently built and what is planned.

### Current
- **FastAPI** handles routing and request validation via Pydantic schemas
- **PostgreSQL** with a 3-tier user security model (`admin` / `migration` / `runtime`)
- **Alembic** manages schema migrations
- **Task** model (placeholder — replaced by FinancialTask later)


### Planned
- **FinancialTask** model with explicit status lifecycle and `Decimal` precision for all monetary values
- **AuditLog** model records every state change as an immutable history
- **State machine** enforcing valid task transitions (`created → validated → approved → executed → completed → failed`)
- **Idempotency keys** to prevent double-execution
- **Rule engine** for deterministic policy checks (spend limits, approved vendors, time windows)
- **AI decision service** that classifies and prioritizes tasks — output is always validated against rules before anything proceeds
- **Human-in-the-loop approval** for high-value tasks, dry-run mode, and an admin kill switch

---

## Safety Model

Fio is designed so that the AI never unilaterally triggers a financial action. Every AI suggestion passes through two layers before execution:

1. **Automated policy checks** — spend limits, vendor allowlists, balance thresholds
2. **Structured approval workflow** — explicit human sign-off for high-value tasks

All state changes will be recorded in an immutable audit log.

> The safety model is partially implemented. Audit logging and schema-level validation will be live shortly. The rule engine, AI layer, and approval workflow will be implemented later.