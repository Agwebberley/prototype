#!/bin/sh
python3 manage.py makemigrations
python3 manage.py migrate
nohup python3 ./Customer/listener.py &
gunicorn --bind 0.0.0.0:8000 prototype.wsgi:application
