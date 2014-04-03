#!/bin/sh
export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_utils;

echo "Datadonors getting user information from devices ...";

PYTHON2_BIN=$(which python2)
if [ -x $PYTHON2_BIN ]; then 
  PYTHON_BIN=$PYTHON2_BIN;
else
  PYTHON_BIN=$(which python);
fi;
$PYTHON_BIN user_linked_data.py