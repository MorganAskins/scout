#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENV_FILE=$DIR/env.sh
source $ENV_FILE
SCOUT_EXE=$DIR/scoutQt.py

python $SCOUT_EXE $@
