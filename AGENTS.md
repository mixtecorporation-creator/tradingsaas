# Trading SaaS Platform — AGENTS.md

**Status:** Greenfield — only this file exists. All structure below is planned, not yet verified by code.

## Planned stack & architecture

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js + React + TypeScript |
| Backend | FastAPI + Python |
| Database | PostgreSQL |
| Cache/queue | Redis |
| Realtime | WebSockets |
| Background jobs | Python workers (Celery or equiv) |
| Deployment | Docker |

- **Modular monolith** — domains isolated by folder, not microservices.
- **WebSockets** for live data & collaboration.
- **PG** for business data, **Redis** for caching/queues/ephemeral state.

## 10 domain modules

Each lives in `backend/app/domains/<name>/` and `frontend/modules/<name>/`:

1. Auth & accounts
2. Dashboard & app shell
3. Live charts & market data
4. Trade journaling
5. Strategy backtesting
6. Trader profiles & verification
7. Leaderboards & reputation
8. Subscriptions & monetization
9. AI insights & analytics
10. Community & collaboration

## Project layout (to scaffold)

```
trading/
  frontend/
    app/             # App Router routes
    components/      # Shared UI
    lib/             # API clients, hooks, utils
    modules/         # Mirror backend domains
  backend/
    app/
      api/           # FastAPI route handlers
      core/          # Config, middleware, DB session
      domains/       # One package per domain
    workers/
    tests/
  docker/
  scripts/
```

## Development

```bash
frontend$ npm install && npm run dev
backend$  python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload
stack$    docker compose up
```

Verification order: **lint → typecheck** (`tsc --noEmit` / `mypy .`) → **test** (`pytest` / `vitest`).

## Conventions

- TypeScript everywhere on frontend. Pydantic schemas on backend. Typed contracts across the boundary.
- Small reusable components. Web first, desktop later.
- Reuse patterns over new abstractions. No unnecessary dependencies.
- Trader-focused UI: clean, modern, responsive.

## Build sequence

1. Auth & onboarding → workspace shell
2. Charts & live market data
3. All other modules in priority order above

## Decision check

Does the feature improve **trust, retention, learning, or monetization**? Build the minimum version that proves value. Verified performance is the moat.
