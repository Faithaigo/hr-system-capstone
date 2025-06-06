# Stage 1: Base build stage
FROM python:3.12-alpine AS builder

# Install system dependencies for mysqlclient and build tools
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-dev \
    pkgconf \
    build-base \
    libffi-dev \
    && rm -rf /var/cache/apk/*

# Create app directory
RUN mkdir /app
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-alpine

# Add runtime dependencies only (no compilers)
RUN apk add --no-cache \
    libffi \
    mariadb-dev \
    && rm -rf /var/cache/apk/*

# Create app user and directory
RUN adduser -D appuser && mkdir /app && chown -R appuser /app

# Copy Python dependencies
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set workdir and copy app
WORKDIR /app
COPY --chown=appuser:appuser . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "hrsystem.wsgi:application"]
