#!/bin/bash
set -e

touch .env.example
touch .gitignore
touch pyproject.toml
touch requirements.txt
touch README.md

mkdir -p docs
touch docs/installation.md
touch docs/trace-viewer.md
touch docs/debug.md
touch docs/codegen.md

mkdir -p config
touch config/__init__.py
touch config/settings.py

mkdir -p pages
touch pages/__init__.py
touch pages/base_page.py

mkdir -p fixtures
touch fixtures/__init__.py
touch fixtures/auth.py
touch fixtures/common.py
touch fixtures/pages.py

mkdir -p utils
touch utils/__init__.py
touch utils/api_client.py
touch utils/helpers.py

mkdir -p tests
touch tests/__init__.py
touch tests/conftest.py

mkdir -p tests/e2e/use_cases
touch tests/e2e/__init__.py
touch tests/e2e/conftest.py
touch tests/e2e/use_cases/__init__.py

mkdir -p tests/e2e/user_stories
touch tests/e2e/user_stories/__init__.py

mkdir -p tests/integration/use_cases
touch tests/integration/__init__.py
touch tests/integration/conftest.py
touch tests/integration/use_cases/__init__.py

mkdir -p tests/integration/user_stories
touch tests/integration/user_stories/__init__.py

mkdir -p tests/api
touch tests/api/__init__.py
touch tests/api/conftest.py

mkdir -p reports/traces
mkdir -p reports/screenshots
mkdir -p reports/html

touch reports/.gitkeep
