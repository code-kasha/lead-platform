# syntax=docker/dockerfile:1

# One image serves everything: the Django API, the admin, and the built
# React app (same origin, so the frontend calls /api directly).

# ------------------------------------------------------------------------------
# Stage 1: build the frontend (static files, so it runs on the build machine's
# own platform even when the image is built for another one)
# ------------------------------------------------------------------------------
FROM --platform=$BUILDPLATFORM node:22-slim AS frontend

WORKDIR /app/frontend

RUN npm install --global pnpm@10.33.0

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY frontend/ ./

# Baked in at build time: the API is served from the same origin
ENV VITE_API_URL=/api
RUN pnpm build

# ------------------------------------------------------------------------------
# Stage 2: runtime
# ------------------------------------------------------------------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_ENV=production \
    PORT=8000

WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

COPY backend/ ./
COPY --from=frontend /app/frontend/dist ./frontend_dist

# Pre-compress the frontend (gzip) so WhiteNoise serves smaller files
RUN python -m whitenoise.compress frontend_dist

# Collect admin/DRF static files. The values below exist only so production
# settings load during the build; real ones come from the host at runtime.
RUN SECRET_KEY=build-only \
    DATABASE_URL=sqlite:///:memory: \
    ALLOWED_HOSTS=build \
    CORS_ALLOWED_ORIGINS=https://build \
    CSRF_TRUSTED_ORIGINS=https://build \
    python manage.py collectstatic --noinput

RUN useradd --create-home --uid 10001 app
USER app

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]
