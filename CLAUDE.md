# Server Adoption Agency — Django demo

A shelter for servers abandoned when their owners moved to the cloud. Built as a live demo showcasing Uncloud.

## Running locally

```bash
mise install
uv sync
uv run python manage.py migrate
uv run python manage.py seed_shelter   # populates 6 servers
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

## Running tests

```bash
uv run python manage.py test shelter
```

## Stack

- Django 6, Postgres 18 (SQLite fallback for local dev), gunicorn
- HTMX and Tailwind via CDN — no build step
- `django-htmx` middleware for `request.htmx` detection
- Pillow for portrait `ImageField`; portraits stored as bytea in Postgres via `django-db-file-storage` (no media volume)
- uv for dependency management
- mise for dev environment management (Python, uv, pre-commit versions pinned in `.mise.toml`)

## Project layout

- `server_adoption/` — Django project package (settings, root urls, wsgi)
- `shelter/` — the single app (models, views, forms, admin, templates, templatetags)
- `shelter/management/commands/seed_shelter.py` — idempotent seed with 6 hand-written servers
- `shelter/management/commands/img/` — source portrait PNGs the seed loads into the DB, one per slug
- `shelter/templates/shelter/partials/` — HTMX swap targets (server grid, application form, thanks)
- `shelter/templatetags/shelter_extras.py` — `species_emoji`, `species_accent`, `species_bg`, and `add_class` template filters
- `shelter/storage.py` — `InlineDatabaseFileStorage` subclass that serves portraits inline (no attachment header)

## Key conventions

- All views are function-based. Keep it that way for demo readability.
- HTMX-aware views return partials when `request.htmx`, full pages otherwise.
- `AdoptionApplication` uses a UUID primary key (shareable status URL). Fields: applicant contact info, decibel tolerance, why_this_server.
- The admin `approve_selected` action is the main staff workflow — it flips application to Approved, stamps the server Adopted, and copies the applicant name. Keep it in one action, not split.
- `seed_shelter` uses `get_or_create` on slug — safe to run multiple times.
- No comments unless the reason is non-obvious.
- Use type hints on all functions and methods. Prefer modern Python syntax: `X | Y` unions, `list[X]`/`dict[K, V]` built-in generics, `str | None` over `Optional[str]`.

## Deployment

`compose.yaml` is ready for `uc deploy`. Named volumes `db` and `media` survive redeploys. See README for the TODO section on wiring up `uc machine add`.

## Out of scope (don't add)

- Multi-user auth beyond Django admin
- Email sending in prod (console backend is fine)
- Foster program, success stories, donations, volunteers
- Internationalisation
- Postgres migration
