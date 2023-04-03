# Render.com buildscript
set -o errexit

sudo apt-get install python-dev
sudo apt-get install python3-dev

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations && python manage.py migrate
