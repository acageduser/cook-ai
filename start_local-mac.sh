#!/bin/bash
# Change to the directory where the script is located
cd "$(dirname "$0")"

#create virtual environment
python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# run Flask application
flask run
