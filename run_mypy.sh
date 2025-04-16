#!/bin/bash

ADDITIONAL_WITHS="--with types-PyYAML --with pytest --with markdown-it-py --with mdformat --with types-click"

while true; do
    # rerun script whenever anything changes in the spicy or tests folders
    find src/spicy tests | sed '/__pycache__/d' > .ruff_files
    cat .ruff_files | entr -d bash -c "clear && uvx ${ADDITIONAL_WITHS} mypy --strict src/spicy tests"
    rm .ruff_files
    # sleep for four seconds so we have a chance to quit
    sleep 4
done
