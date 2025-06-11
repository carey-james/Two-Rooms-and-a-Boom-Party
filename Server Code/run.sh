# Setup the Python Virtual Environment 
python3 -m venv myvenv
source myvenv/bin/activate
# Upgrade Pip
python -m pip install --upgrade pip
# Get required packages
pip install -r requirements.txt
# Migrations for Django
python manage.py makemigrations
python manage.py migrate
# Start the server
python manage.py runserver 0.0.0.0:8000
