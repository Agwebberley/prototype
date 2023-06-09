#!/bin/sh     
sudo git pull origin main
sudo pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
sudo systemctl restart nginx
sudo systemctl restart gunicorn
python manage.py start_listeners &