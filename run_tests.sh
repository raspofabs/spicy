#!/bin/bash

while true; do
    # rerun script whenever anything changes in the spicy or tests folders
    find src/spicy tests | sed '/__pycache__/d' > .test_files
    cat .test_files | entr -d uv run tests/z_run.sh ;
    rm .test_files
    # sleep for four seconds so we have a chance to quit
    sleep 4
done
