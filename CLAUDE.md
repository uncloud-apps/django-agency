# Server Adoption Agency — Django demo

A shelter for servers abandoned when their owners moved to the cloud. Built as a live demo for a Django meetup talk showcasing Uncloud.

## Running locally

```bash
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

All 28 tests should pass.

## Stack

- Django 6, SQLite, gunicorn
- HTMX and Tailwind via CDN — no build step
- `django-htmx` middleware for `request.htmx` detection
- Pillow for portrait `ImageField`
- uv for dependency management

## Project layout

- `server_adoption/` — Django project package (settings, root urls, wsgi)
- `shelter/` — the single app (models, views, forms, admin, templates, templatetags)
- `shelter/management/commands/seed_shelter.py` — idempotent seed with 6 hand-written servers
- `shelter/templates/shelter/partials/` — HTMX swap targets (server grid, application form, thanks)
- `shelter/templatetags/shelter_extras.py` — `species_emoji` and `add_class` template filters
- `media/portraits/` — AI-generated server portraits, gitignored, one per slug

## Key conventions

- All views are function-based. Keep it that way for demo readability.
- HTMX-aware views return partials when `request.htmx`, full pages otherwise.
- `AdoptionApplication` uses a UUID primary key (shareable status URL).
- The admin `approve_selected` action is the main staff workflow — it flips application to Approved, stamps the server Adopted, and copies the applicant name. Keep it in one action, not split.
- `seed_shelter` uses `get_or_create` on slug — safe to run multiple times.
- No comments unless the reason is non-obvious.

## Deployment

`compose.yaml` is ready for `uc deploy`. Named volumes `db` and `media` survive redeploys. See README for the TODO section on wiring up `uc machine add`.

## Out of scope (don't add)

- Multi-user auth beyond Django admin
- Email sending in prod (console backend is fine)
- Foster program, success stories, donations, volunteers
- Internationalisation
- Postgres migration
