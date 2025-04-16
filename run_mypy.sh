#!/bin/bash

ADDITIONAL_WITH_OPTIONS="--with types-PyYAML --with pytest --with markdown-it-py --with mdformat --with types-click"

while true; do
    # rerun script whenever anything changes in the spicy or tests folders
    find src/spicy tests | sed '/__pycache__/d' > .ruff_files
    OFFLINE="--offline"
    cat .ruff_files | entr -d bash -c "clear && uvx ${OFFLINE} ${ADDITIONAL_WITH_OPTIONS} mypy --strict src/spicy tests"
    rm .ruff_files
    # sleep for four seconds so we have a chance to quit
    sleep 4
done
