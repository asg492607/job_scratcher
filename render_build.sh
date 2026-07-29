#!/usr/bin/env bash
# exit on error
set -o errexit

cd backend
pip install --upgrade pip
pip install -r requirements.txt

# Set Playwright browser path locally to avoid system permission issues on Render
export PLAYWRIGHT_BROWSERS_PATH=0
python -m playwright install chromium
