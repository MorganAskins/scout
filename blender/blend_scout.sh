#!/bin/bash

# This shell script creates the various blender objects, then builds scout from them
# This is basically a hack since import doesn't seem to work
# 
function blend {
    echo "blend has $# arguments"
    for arg in "$@"
    do
	goodness=$(check_arg "$arg")
	if [ "$goodness" == "true" ]
	then
	    echo "trueness"
	fi
    done
    blender --python scout.py
}

function check_arg {
    # If the argument is not in the list of accepted arguments remove it
    declare -a good_args=("run")
    local is_good=false
    for arg in "${good_args[@]}"
    do
	if [ "$arg" == "$1" ]
	then
	    is_good=true
	fi
    done
    echo "$is_good"
}

export BLENDER_USER_SCRIPTS=`pwd`/scripts
blend $@
