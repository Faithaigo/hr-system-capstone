#!/bin/sh

# Get database host from environment variable
DB_HOST="$DATABASE_HOST" # Use the environment variable here

echo "Waiting for postgres at $DB_HOST..."

# Use the environment variable in the nc command
while ! nc -z "$DB_HOST" 5432; do
  echo "Postgres at $DB_HOST not yet ready, sleeping..."
  sleep 0.5
done

echo "PostgreSQL started at $DB_HOST"

# Apply database migrations
python manage.py migrate --noinput # Added --noinput for non-interactive builds

# Start the Django application
exec "$@"