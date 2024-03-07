#!/bin/bash

server=$(netstat -ano | grep 8000)

if [ "${server}" ]
then
        echo true > logs/status.log
        echo $server >> logs/status.log
else
        echo false > logs/status.log
        echo $(date +"%Y-%m-%d %H:%M") >> ~/logs/cron.log
        python3 ~/MacMailing/app/manage.py runserver 0.0.0.0:8000>>logs/$(date +"%Y-%m-%d").log &
fi
