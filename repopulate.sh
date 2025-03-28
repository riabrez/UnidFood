#!/bin/bash

set -e

PROJ_DIR="unidfood_project"

if [ -d "$PROJ_DIR" ]; then
    cd "$PROJ_DIR"
    echo "Changed to directory: $PROJ_DIR"
else
    echo -e "$Error: Directory $PROJ_DIR not found$"
    exit 1
fi


echo -e "Starting unidfood database reset...$"

# Delete the SQLite database file
if [ -f "db.sqlite3" ]; then
    echo "Removing existing database..."
    rm db.sqlite3
    echo "Database removed successfully"
else
    echo "No existing database found"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate
echo -e "Migrations completed"

# Create superuser with defaults (username: admin, email: admin@example.com, password: admin)
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
echo -e "Superuser created (username: admin, password: admin)"

# Run population script
if [ -f "population_script.py" ]; then
    echo "Running population script..."
    python population_script.py
    echo -e "Population script completed"
else
    echo -e "Error: population_script.py not found"
    exit 1
fi

echo -e "UnidFood database reset successfully!"