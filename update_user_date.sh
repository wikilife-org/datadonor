#!/bin/sh
export PYTHONPATH=$PYTHONPATH:/usr/local/datadonor_env/lib/python2.7/site-packages:/home/datadonor:/home/wikilife_utils;

echo "Datadonors getting user information from devices ...";

cd /home/datadonor
python manage.py get_user_data
