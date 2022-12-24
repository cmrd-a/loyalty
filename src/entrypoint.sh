#!/bin/bash
echo "Waiting for postgres..."
    while ! nc -z "$POSTGRES_DB_HOST" "$POSTGRES_DB_PORT"; do
      sleep 0.1
    done
echo "PostgreSQL started"

alembic -c alembic.ini upgrade head
python main.py