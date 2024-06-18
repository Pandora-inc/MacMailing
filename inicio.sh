#!/bin/bash
nohup python3 ~/MacMailing/app/manage.py runserver 0.0.0.0:8000 &


crontab -e
*/5 * * * * sh ~/MacMailing/heartbeat.sh
@reboot nohup python3 ~/projets/MacMailing/app/manage.py runserver 0.0.0.0:8000>logs/$(date +"%Y-%m-%d").log &


