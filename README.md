# Flask-RestX_API_Demo Flask vs FastAPI (Sync vs Async)

A teaching project comparing synchronous and asynchronous API handling,
using identical data and endpoint logic across two frameworks.

You get to access RPG items here!

## What this demonstrates

Same database, same three endpoint types, two different concurrency models:

| | Flask (this repo) | FastAPI (this repo) |
|---|---|---|
| Server | waitress (WSGI) | uvicorn (ASGI) |
| Concurrency model | OS threads (or none, if `threads=1`) | event loop (`async`/`await`) |
| External API call | `requests` (blocking) | `httpx.AsyncClient` (non-blocking) |

## Project structure

- `shared/` — single source of truth for both apps
  - `schema.sql` / `seed_db.py` — builds `rpg_items.sqlite3` (~300 RPG items: weapons, armor, healing, misc)
  - `models.py` — plain SQLAlchemy declarative models, imported by both apps
  - `mock_external_api.py` — simulates a slow third-party API (deliberate delay), used by the `/roll` endpoint on both sides
  - `benchmark.py` — fires N concurrent requests at either app and times the batch
- `flask_app/` — Flask-RESTX implementation
- `fastapi_app/` — FastAPI implementation, same endpoints, `async def` where it matters

## Setup

Each app has its own venv (Python 3.11+ recommended):

\```
cd flask_app
python -m venv .venv # Windows
.venv\Scripts\Activate.ps1

pyhton3 -m venv .venv # Linux
source .venv/bin/activate

pip install -r requirements.txt
\```

Repeat for `fastapi_app/`.

Build the database once (either venv works, uses only stdlib):
\```
python shared\seed_db.py
\```

## Running it — you need 3 terminals

All commands run from the **repo root**, with the relevant venv activated:

1. Mock external API (port 9000):
   \```
   python -m shared.mock_external_api
   \```
2. Flask app (port 8000):
   \```
   python -m flask_app.app
   \```
3. FastAPI app (port 8001):
   \```
   python -m fastapi_app.main
   \```

Swagger docs: `http://localhost:8000/` (Flask), `http://localhost:8001/docs` (FastAPI)

## Endpoints (identical shape on both apps)

- `GET /items/` — list first 20 items
- `GET /items/<id>` — item detail, **2 database queries** (item + its type-specific stats via a relationship)
- `GET /items/<id>/roll` — item lookup + **1 external network call** to the mock API (the endpoint that shows the sync/async difference)

## Running the benchmark

With all 3 servers running, in a 4th terminal:
\```
python -m shared.benchmark flask
python -m shared.benchmark fastapi
\```

Fires 5 concurrent requests at `/items/32/roll` and times the whole batch.

### Actual results from this repo

\```
Flask (sync, single-threaded waitress):   35.54s for 5 requests (~7s apart, fully serial)
FastAPI (async, uvicorn):                  5.68s for 5 requests (~6x faster)
\```

## The lesson

One request alone looks identical on both servers — the difference **only** shows up under
concurrent load, because that's when blocking I/O (`requests.get`, waiting on the mock API)
either stalls everything behind it (sync) or lets the event loop serve other requests during
the wait (async).

## Known gotchas (found the hard way — worth knowing before you rebuild this)

- **Flask's dev server (`app.run()`) does not reliably behave "single-threaded by default"
  on all Werkzeug versions.** Use `waitress.serve(app, host="0.0.0.0", port=8000, threads=1)`
  for a guaranteed serial baseline, and `threads=N` to demonstrate thread-based concurrency.
- **The mock external API is also a Flask app — it needs `threaded=True` in its own
  `app.run(...)`, or *it* becomes the bottleneck regardless of how the calling app handles concurrency.**
- **`httpx.AsyncClient()` has a 5-second default timeout.** Set `timeout=30.0` (or higher)
  explicitly if your mock delay is anywhere near or above that, or you'll see spurious
  `ReadTimeout` / 500 errors that look like a bug but are actually just an unconfigured timeout.
- gunicorn does not run on native Windows (needs `fcntl`, Unix-only) — waitress is the
  cross-platform equivalent used here instead, and works identically on Windows and Linux.

## Deployment

This project runs directly via Python venvs (see Setup above) — no containerization.
Docker was considered but skipped: since the benchmark relies on multiple processes
talking to each other over `localhost` (main app → mock external API), containerizing
would require solving inter-container networking for no benefit to the actual teaching
goal. Running as plain OS processes keeps the setup mechanical and identical across
Windows and Linux.

## Cross-platform notes

Repo uses `.gitattributes` to normalize line endings (LF) regardless of OS. Built and tested
on Windows 11, verified to run identically on Linux (see gotchas above — nothing OS-specific
in the actual app code, only in server startup flags).
