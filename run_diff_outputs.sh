#!/bin/bash

TEST_SPEC=tests/test_data/cookie_spec

while true; do
    # rerun script whenever anything changes in the spicy or tests folders
    find src/spicy $TEST_SPEC | sed '/__pycache__/d' > .spec_check_files
    cat .spec_check_files | entr -d bash diff_outputs.sh
    rm .spec_check_files
    # sleep for four seconds so we have a chance to quit
    sleep 4
done
