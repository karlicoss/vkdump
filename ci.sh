#!/bin/bash

cd "$(this_dir)" || exit

. ~/bash_ci

PYTHON="python3.6"

ci_run $PYTHON -mpylint -E vkdump
ci_run $PYTHON -mmypy vkdump
ci_run with_secrets $PYTHON test.py

ci_report_errors
