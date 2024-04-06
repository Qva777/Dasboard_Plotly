#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
while ! nc -z postgres 5432; do
    sleep 1
done
echo "PostgreSQL is ready."


#  Fix bug with Plotly style
echo "Opening Folder with templatetags"
cd /usr/local/lib/python3.11/site-packages/django_plotly_dash/templatetags

echo "Commenting style"
sed -i 's/position: relative;/# position: relative;/' plotly_dash.py

echo "Back to main folder"
cd /app


# Creating .env file
echo "Creating .env file..."
cat <<EOL > .env
# Django configuration
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=10

# PostgreSQL (docker/local)
DB_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=admin_dash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
DB_PORT=5432

# pgadmin container
PGADMIN_DEFAULT_EMAIL=admin@gmail.com
PGADMIN_DEFAULT_PASSWORD=root
EOL

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate --skip-checks

# Apply fixtures
echo "Applying apps fixtures"
python manage.py loaddata fixtures/products.json
python manage.py loaddata fixtures/clients.json
python manage.py loaddata fixtures/countries.json
python manage.py loaddata fixtures/orders.json

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000



