#!/bin/bash

TEST_SPEC=tests/test_data/cookie_spec

clear
uv run oldspice $TEST_SPEC > old.txt
uv run newspice $TEST_SPEC > new.txt
diff --color old.txt new.txt
