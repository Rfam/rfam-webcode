# Base image - Python with Node.js for frontend build
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    curl \
    netcat-openbsd \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application source from build context
COPY rfam-webcode/ .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Install Node.js dependencies and build frontend assets
RUN npm install && npm run build

# Collect static files
RUN RFAM_DB_HOST=localhost DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput 2>/dev/null || true

# Copy startup script
COPY startup.sh /usr/local/bin/startup.sh
RUN chmod +x /usr/local/bin/startup.sh

# Clean up build dependencies
RUN apt-get purge -y gcc pkg-config && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /root/.cache

# Add labels
LABEL maintainer="Rfam Team"
LABEL org.opencontainers.image.title="Rfam Web API"
LABEL org.opencontainers.image.description="Rfam RNA families database - Django REST API"
LABEL org.opencontainers.image.url="https://github.com/Rfam/rfam-django-K8s"
LABEL org.opencontainers.image.source="https://github.com/Rfam/rfam-django-K8s"

# Expose port
EXPOSE 8000

# Default entrypoint
ENTRYPOINT ["/usr/local/bin/startup.sh"]
