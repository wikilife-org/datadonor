#!/bin/sh
export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_v4/wikilife_utils;

echo "Datadonors server starting ...";

PYTHON2_BIN=$(which python2)
if [ -x $PYTHON2_BIN ]; then 
  PYTHON_BIN=$PYTHON2_BIN;
else
  PYTHON_BIN=$(which python);
fi;

$PYTHON_BIN manage.py runserver 8080 --settings=local_settings
echo "Server Started";
