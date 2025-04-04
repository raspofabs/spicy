#!/bin/bash

while true; do
    # rerun script whenever anything changes in the spicy or tests folders
    find src/spicy tests/test_data | sed '/__pycache__/d' > .spec_check_files
    cat .spec_check_files | entr -d bash -c "clear && uv run spicy tests/cookie_spec"
    rm .spec_check_files
    # sleep for four seconds so we have a chance to quit
    sleep 4
done
