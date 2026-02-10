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

# Set build arguments for flexibility
ARG REPO_URL=https://github.com/Rfam/rfam-webcode.git
ARG BRANCH=main
ARG USE_LOCAL_SOURCE=false

# Copy source code - either from local context or git clone
RUN if [ "$USE_LOCAL_SOURCE" = "true" ]; then \
        echo "Using local source code..."; \
        mkdir -p /app; \
    else \
        echo "Cloning source code from git..."; \
        apt-get update && apt-get install -y git && \
        git clone --depth 1 --branch ${BRANCH} ${REPO_URL} /tmp/rfam-source || \
        git clone --depth 1 --branch main ${REPO_URL} /tmp/rfam-source || \
        git clone --depth 1 ${REPO_URL} /tmp/rfam-source; \
        mkdir -p /app && cp -r /tmp/rfam-source/rfam-webcode/* /app/ && rm -rf /tmp/rfam-source; \
        apt-get purge -y git && apt-get autoremove -y; \
    fi

# Copy local source if using local mode
COPY . /tmp/local-source/
RUN if [ "$USE_LOCAL_SOURCE" = "true" ]; then \
        cp -r /tmp/local-source/rfam-webcode/* /app/ 2>/dev/null || \
        cp -r /tmp/local-source/* /app/; \
    fi && \
    rm -rf /tmp/local-source

# Set working directory
WORKDIR /app

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
