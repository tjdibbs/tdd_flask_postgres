#!/bin/sh

echo "Waiting for postgres server to start..."

# nc -z app-db 5432 command check the container there is any network name app-db running
# app-db is the name of the network instead of the ip
while ! nc -z app-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# Methods to run the app

# ----- 1 ----
#export FLASK_APP=main
#flask init-db
#flask run -h 0.0.0.0

# ----- 2 ------
#python manage.py --app main init-db
#python manage.py --app main run -h 0.0.0.0

# ----- 3 -----
export FLASK_APP=main
python manage.py init-db
python manage.py run -h 0.0.0.0