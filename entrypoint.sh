#!/bin/sh

echo "Waiting for postgres..."

# nc -z app-db 5432 command check the container there is any network name app-db running
# app-db is the name of the network instead of the ip
while ! nc -z app-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

flask --app main init-db
flask --app main run -h 0.0.0.0
