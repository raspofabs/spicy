#!/bin/bash

COVERAGE_PARAMS="--cov=spicy --no-cov-on-fail --cov-report term-missing:skip-covered --cov-branch --cov-report html tests/"
PYTEST_PARAMS="--durations=3 -vv"
#PYTEST_PARAMS="--durations=3 -n auto"

uv run pytest $PYTEST_PARAMS -m "not gui" $COVERAGE_PARAMS
