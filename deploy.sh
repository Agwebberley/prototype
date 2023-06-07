#!/bin/sh     
sudo git pull origin master
sudo pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
sudo systemctl restart nginx
sudo systemctl restart gunicorn
nohup python3 ./Customer/listener.py &
gunicorn --bind 0.0.0.0:8000 prototype.wsgi:application
