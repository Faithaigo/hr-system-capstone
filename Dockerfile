# Stage 1: Base build stage
FROM python:3.12-alpine AS builder

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

# Create app user and directory
RUN adduser -D appuser && mkdir /app && chown -R appuser /app

# Copy Python dependencies
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/


# Install netcat-openbsd for entrypoint.sh (using apk for Alpine)
RUN apk update && apk add --no-cache netcat-openbsd

# Set workdir and copy app
WORKDIR /app
COPY --chown=appuser:appuser . .

# Set a dummy SECRET_KEY for collectstatic during build
# This value is only used during the build and is not exposed in the final image or at runtime
# The actual SECRET_KEY will be provided via docker-compose at runtime
RUN DJANGO_SECRET_KEY=not-a-real-key-for-build-time python manage.py collectstatic --noinput

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy and prepare entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "hrsystem.wsgi:application"]
