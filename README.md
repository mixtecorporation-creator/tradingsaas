# TradeSaaS

All-in-one trading workspace — live charts, trade journaling, backtesting, verified profiles, leaderboards, and community.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional, for PostgreSQL/Redis/Minio)

## Quick Start

### Backend

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 -m app.seed      # seed demo data (demo@trading.com / demo1234)
uvicorn app.main:app --reload
```

API at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App at `http://localhost:3000`.

### Docker (full stack)

```bash
docker compose up
```

This starts PostgreSQL, Redis, Minio, backend, worker, and frontend.

## Demo Credentials

- **Email:** demo@trading.com
- **Password:** demo1234

## Scripts

### Backend (`backend/`)

| Command | Description |
|---------|-------------|
| `uvicorn app.main:app --reload` | Start dev server |
| `python -m app.seed` | Seed demo data |
| `pytest` | Run tests |
| `alembic upgrade head` | Run migrations |

### Frontend (`frontend/`)

| Command | Description |
|---------|-------------|
| `npm run dev` | Dev server |
| `npm run build` | Production build |
| `npm run lint` | Lint check |
| `npm run typecheck` | TypeScript check |

## Project Structure

```
trading/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers
│   │   ├── core/         # Config, middleware, DB session
│   │   ├── domains/      # Auth, trades, instruments, etc.
│   │   └── models/       # SQLAlchemy models
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app/              # Next.js App Router pages
│   ├── components/       # Shared UI components
│   ├── lib/              # Hooks, API client, utils
│   └── stores/           # Zustand stores
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── AGENTS.md
```
# tradingsaas
