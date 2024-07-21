@echo off

:: Starting Local Server
echo.
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                               Starting Local Server                        +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.

:: Change to the directory where the script is located
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                        Changing to the Script Directory                    +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
cd /d "%~dp0"

:: Check if Python 3.12 is installed
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                          Checking for Python 3.12                          +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
python --version 2>nul | findstr /r "^Python 3.12" >nul
if %ERRORLEVEL% neq 0 (
    echo Python 3.12 not found, please install it manually and ensure it's added to PATH.
    pause
    exit /b 1
) else (
    echo Python 3.12 is already installed.
)

:: Ensure the specific version of pip (24.1.2) is installed
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                         Installing pip 24.1.2                              +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
python -m ensurepip --upgrade
python -m pip install --upgrade pip==24.1.2

:: Create a virtual environment
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                          Creating Virtual Environment                      +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
python -m venv venv

:: Activate the virtual environment
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                         Activating Virtual Environment                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
call venv\Scripts\activate

:: Install Flask
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                              Installing Flask                              +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install Flask

:: Install the required dependencies
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                       Installing Required Dependencies                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install -r requirements.txt

:: Upgrade to a specific version of the OpenAI API
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                  Upgrading to a Specific Version of OpenAI API             +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install openai==1.35.15

:: Install additional libraries
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                        Install Pillow and requests                         +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install Pillow requests

:: Run the Flask application
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                          Running the Flask Application                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
flask run
