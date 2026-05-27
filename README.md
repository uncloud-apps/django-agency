# Server Adoption Agency

> **Demo app** — not intended for production use. SECRET_KEY is committed, and there is no real auth beyond Django admin.

A Django demo app to showcase Uncloud: a shelter for abandoned servers whose previous owners moved to the cloud.

<img width="1396" height="719" alt="image" src="https://github.com/user-attachments/assets/acaf34b5-6a6b-401c-8f24-a97a4be0c7d9" />

Built with Django 6, HTMX, Tailwind (CDN), Postgres 18 (SQLite fallback for local dev). Dev environment managed with mise (`.mise.toml` pins Python, uv, and pre-commit versions).

Developed with AI assistance.

## Run locally

```bash
# Install all dev tools
mise install

# Install dependencies
uv sync

# Apply migrations
uv run python manage.py migrate

# Seed with 6 example servers (optional)
uv run python manage.py seed_shelter

# Create an admin account (optional)
uv run python manage.py createsuperuser

# Start the dev server
uv run python manage.py runserver
```

Visit http://localhost:8000 for the shelter, http://localhost:8000/admin for the staff portal.

## Adding server portraits

Drop AI-generated PNGs into `shelter/management/commands/img/<slug>.png` (one per server slug). `seed_shelter` reads them and stores them as bytea in Postgres via `django-db-file-storage`. New uploads via the admin go to the same storage automatically — there is no `media/` directory.

## Deploying to Uncloud

Copy `.env.example` to `.env` and fill in `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD`:

```bash
cp .env.example .env
# Edit .env with real values
```

The `compose.yaml` is ready. Run `uc machine init` to initialise your cluster, then `uc deploy` to deploy.
The Postgres data and media files use named volumes so they survive redeploys.
