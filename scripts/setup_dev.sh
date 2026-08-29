#!/usr/bin/env bash
# Configure l'environnement de developpement pour omega-check.
# Suppose que ~/DEV/LIB/omega-lib existe deja (voir README.md).
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -e ../../LIB/omega-lib
pip install --quiet -e ".[dev]"

echo "Environnement pret. Verification :"
lint-imports
pytest -q
ruff check src tests
mypy -p omega_check
