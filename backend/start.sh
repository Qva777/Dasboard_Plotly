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

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000



