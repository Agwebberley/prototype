#!/bin/sh     
sudo git pull origin main
sudo pip3 install -r requirements.txt
sudo systemctl restart nginx
sudo systemctl restart gunicorn
sudo python3 manage.py start_listeners &