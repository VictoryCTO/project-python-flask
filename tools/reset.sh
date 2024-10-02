#!/bin/bash

# This script is used to reset the database to the initial state and remove
# app cache files

# Remove cache files
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -exec rm -rf {} +


# move exec of the script to the directory above the tools directory
# regardless of where the script is called from
cd "$(dirname "$0")/.."

rm -rf migrations
rm -rf instance
poetry run flask db init
poetry run flask db migrate
poetry run flask db upgrade
