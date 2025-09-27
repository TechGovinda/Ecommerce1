    #!/bin/bash
    # echo "Building the project..."
    # python3.9 -m pip install -r requirements.txt
    # echo "Make Migration..."
    # python3.9 manage.py makemigrations --noinput
    # python3.9 manage.py migrate --noinput
    # echo "Collect Static..."
    # python3.9 manage.py collectstatic --noinput --clear


    #!/bin/bash
set -e

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
echo "Build completed successfully."
    