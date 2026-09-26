#!/bin/sh
# Container start: apply migrations, create the first admin if configured,
# then serve. Hosts without a pre-deploy hook (e.g. Render's free plan) rely
# on this running migrations on every start; both steps are idempotent.
set -e

python manage.py migrate --noinput
python manage.py ensure_superuser

# 2 workers fit comfortably in a 512 MB free instance
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT}" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
