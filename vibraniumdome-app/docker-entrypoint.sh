#!/bin/bash
wait_for_db() {
  echo "Waiting for the database to be ready..."
  while ! mysqladmin ping -h"vibraniumdome-app-db" --silent; do
    sleep 1
  done
}

wait_for_db

echo "Database is up - running db commands..."
npm run db:push
npm run db:seed
echo "Database is up - done running db commands :D"

exec "$@"