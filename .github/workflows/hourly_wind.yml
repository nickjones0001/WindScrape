name: Hourly Wind Update

on:
  schedule:
    # This runs at the start of every hour
    - cron: '0 * * * *'
  workflow_dispatch: # Allows you to run it manually for testing

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install gspread google-auth requests

      - name: Run Script
        env:
          GCP_SERVICE_ACCOUNT_JSON: ${{ secrets.GCP_SERVICE_ACCOUNT_JSON }}
        run: python main.py
