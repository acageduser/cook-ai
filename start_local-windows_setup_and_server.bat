#!/bin/bash

echo "Starting Local Server"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                        Changing to the Script Directory                    +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

cd "$(dirname "$0")"

echo "Checking for Python 3.x"
python --version 2>/dev/null | grep -q "^Python 3\."
if [ $? -ne 0 ]; then
    echo "Python 3.x not found. Please install Python 3.12 or any 3.7+ version and ensure it's added to PATH."
    read -p "Press any key to exit..."
    exit 1
fi

echo "Creating Virtual Environment"
python -m venv venv

echo "Activating Virtual Environment"
source venv/Scripts/activate

echo "Installing Flask"
pip install Flask

echo "Installing Required Dependencies"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found"
    read -p "Press any key to exit..."
    exit 1
fi

echo "Running Flask Application"
flask run
