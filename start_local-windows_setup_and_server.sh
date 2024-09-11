#!/bin/bash

# Starting Local Server
echo
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                               Starting Local Server                        +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo

# Change to the directory where the script is located
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                        Changing to the Script Directory                    +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
cd "$(dirname "$0")" || { echo "Failed to change directory"; exit 1; }
echo "Current Directory: $(pwd)"

# Check if Python 3.7+ is installed
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                          Checking for Python 3.7+                          +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
python --version 2>/dev/null | grep -q "^Python 3\.[7-9]\|^Python 3\.1[0-9]"
if [ $? -ne 0 ]; then
    echo "Python 3.7+ not found, please install Python 3.7 or above and ensure it's added to PATH."
    read -p "Press any key to exit..." 
    exit 1
else
    echo "Compatible Python 3.7+ version is already installed."
fi

# Create a virtual environment
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                          Creating Virtual Environment                      +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
python -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    read -p "Press any key to exit..." 
    exit 1
fi

# Activate the virtual environment
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                         Activating Virtual Environment                     +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Virtual environment activation script not found."
    read -p "Press any key to exit..." 
    exit 1
fi

# Ensure pip is installed and the correct version
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                         Ensuring pip 24.2 is Installed                     +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
python -m ensurepip --upgrade 2>/dev/null
python -m pip install --upgrade pip==24.2
python -m pip --version 2>/dev/null | grep -q "pip 24.2"
if [ $? -ne 0 ]; then
    echo "Failed to install pip 24.2. Please check your Python installation."
    deactivate
    exit 1
else
    echo "pip 24.2 is successfully installed."
fi

# Install Flask
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                              Installing Flask                              +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
pip install Flask
if [ $? -ne 0 ]; then
    echo "Failed to install Flask. Please check your Python installation."
    deactivate
    exit 1
fi

# Install the required dependencies
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                       Installing Required Dependencies                     +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies from requirements.txt."
        deactivate
        exit 1
    fi
else
    echo "ERROR: requirements.txt not found."
    read -p "Press any key to exit..." 
    deactivate
    exit 1
fi

# Upgrade to a specific version of the OpenAI API
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                  Upgrading to a Specific Version of OpenAI API             +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
pip install openai==1.35.15
if [ $? -ne 0 ]; then
    echo "Failed to install OpenAI API version 1.35.15."
    deactivate
    exit 1
fi

# Install additional libraries
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                        Install Pillow and requests                         +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
pip install Pillow requests
if [ $? -ne 0 ]; then
    echo "Failed to install Pillow and requests."
    deactivate
    exit 1
fi

# Run the Flask application
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                          Running the Flask Application                     +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo
flask run

# Deactivate the virtual environment after usage
deactivate
