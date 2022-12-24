#!/bin/bash
echo "Waiting for postgres..."
    while ! nc -z "$LOYALTY_POSTGRES_HOST" "$LOYALTY_POSTGRES_PORT"; do
      sleep 0.1
    done
echo "PostgreSQL started"

alembic -c alembic.ini upgrade head
python main.py