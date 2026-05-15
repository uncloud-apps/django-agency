# Server Adoption Agency

> **Demo app** — not intended for production use. SECRET_KEY is committed, DEBUG is on, and there is no real auth beyond Django admin.

A Django demo app for the meetup talk. A shelter for abandoned servers whose previous owners moved to the cloud.

Built with Django 6, HTMX, Tailwind (CDN), SQLite.

Developed with AI assistance.

## Run locally

```bash
# Install dependencies
uv sync

# Apply migrations
uv run python manage.py migrate

# Seed with 6 example servers
uv run python manage.py seed_shelter

# Create an admin account
uv run python manage.py createsuperuser

# Start the dev server
uv run python manage.py runserver
```

Visit http://localhost:8000 for the shelter, http://localhost:8000/admin for the staff portal.

## Adding server portraits

Generate AI portraits for each server slug and place them at `media/portraits/<slug>.png`.

After adding portraits, update each server's `portrait` field via the admin or a one-off management command.

## Deploying to Uncloud

TODO: wire this up with `uc deploy`.

The `compose.yaml` is ready. Run `uc machine add` to connect your servers, then `uc deploy` to deploy.
The SQLite database and media files use named volumes so they survive redeploys.
