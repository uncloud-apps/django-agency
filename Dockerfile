FROM python:3.14-slim

RUN apt update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /usr/local/bin/uv

# Create a non-root user app.
RUN useradd --create-home --home-dir /app app
WORKDIR /app
USER app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/usr/local/bin:/usr/bin:/bin" \
    DJANGO_SETTINGS_MODULE=server_adoption.settings \
    WORKERS=2

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY --chown=app:app . .

EXPOSE 8000
HEALTHCHECK --start-period=10s --start-interval=1s CMD curl -f http://localhost:8000

CMD gunicorn server_adoption.wsgi:application --bind 0.0.0.0:8000 --workers ${WORKERS} --access-logfile "-"
