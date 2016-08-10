#!/bin/sh
export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_utils;

echo "Datadonors server starting ...";

python manage.py runserver 8080
echo "Server Started";
