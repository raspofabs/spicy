#!/bin/bash

while true; do
    # rerun script whenever anything changes in the spicy or tests folders
    find src/spicy docs | sed '/__pycache__/d' > .self_check_files
    cat .self_check_files | entr -d bash -c "clear && uv run spicy docs"
    rm .self_check_files
    # sleep for four seconds so we have a chance to quit
    sleep 4
done
