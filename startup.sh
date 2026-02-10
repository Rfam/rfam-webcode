#!/bin/bash
# startup.sh - Django application startup
set -euo pipefail

echo "=== STARTING RFAM DJANGO WEB APPLICATION - BUILD $(date) ==="

# -------------------------------------------------
# Verify Python dependencies
# -------------------------------------------------
echo "=== Verifying installed packages ==="
critical_packages=(
    "django"
    "rest_framework"
    "pymysql"
    "gunicorn"
)

missing_packages=()
for package in "${critical_packages[@]}"; do
    if python -c "import $package" 2>/dev/null; then
        echo "  $package"
    else
        echo "  $package - MISSING"
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "Warning: ${#missing_packages[@]} critical packages are missing:"
    printf "   - %s\n" "${missing_packages[@]}"
    echo "   Application may not function correctly"
fi

# -------------------------------------------------
# Collect static files
# -------------------------------------------------
echo "=== Collecting static files ==="
cd /app
python manage.py collectstatic --noinput 2>/dev/null || echo "Warning: collectstatic failed"

# -------------------------------------------------
# Test database connectivity
# -------------------------------------------------
echo "=== Testing database connectivity ==="
if [ -n "${RFAM_DB_HOST:-}" ]; then
    DB_PORT="${RFAM_DB_PORT:-3306}"
    if nc -z -w 5 "${RFAM_DB_HOST}" "${DB_PORT}" 2>/dev/null; then
        echo "  Database host ${RFAM_DB_HOST}:${DB_PORT} is reachable"

        python -c "
import pymysql
try:
    conn = pymysql.connect(
        host='${RFAM_DB_HOST}',
        port=int('${DB_PORT}'),
        user='${RFAM_DB_USER:-rfamro}',
        password='${RFAM_DB_PASSWORD:-}',
        database='${RFAM_DB_NAME:-Rfam}',
        connect_timeout=5
    )
    conn.close()
    print('  Database connection working')
except Exception as e:
    print(f'  Database connection failed: {e}')
" 2>/dev/null || echo "  Database connection test failed"
    else
        echo "  Database host ${RFAM_DB_HOST}:${DB_PORT} is not reachable"
    fi
else
    echo "  RFAM_DB_HOST not set - using default"
fi

# -------------------------------------------------
# Django system check
# -------------------------------------------------
echo "=== Running Django system checks ==="
python manage.py check --deploy 2>&1 | head -20 || echo "  Some deployment checks reported warnings"

# -------------------------------------------------
# Start application
# -------------------------------------------------
echo "=== Starting Rfam Django application ==="
echo "Application will be available at http://localhost:8000"

cd /app
exec gunicorn rfam_web.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
