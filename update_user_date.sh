#!/bin/sh
export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_utils;

echo "Datadonors getting user information from devices ...";

python manage.py get_user_data