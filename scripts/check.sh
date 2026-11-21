#!/usr/bin/env sh
# Single safe entry point for all local quality gates (read-only except caches).
set -e
echo '== pytest';  python -m pytest -q
echo '== ruff';    ruff check .
echo '== mypy';    mypy expense_splitter
echo '== build';   python -m compileall -q expense_splitter && echo 'compile OK'
