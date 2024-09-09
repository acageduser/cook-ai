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
echo Current Directory: %CD%
cd /d "%~dp0"
echo Changed to Script Directory: %CD%
pause

:: Check if Python 3.x is installed
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                          Checking for Python 3.x                           +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
python --version 2>nul | findstr /r "^Python 3\." >nul
if %ERRORLEVEL% neq 0 (
    echo Python 3.x not found, please install Python 3.12 or any 3.7+ version and ensure it's added to PATH.
    pause
    exit /b 1
) else (
    echo Compatible Python 3.x version is already installed.
)

:: Ensure pip is installed and correct version
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                         Ensuring pip 24.1.2 is Installed                   +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
python -m ensurepip --upgrade 2>nul
python -m pip --version 2>nul | findstr "pip 24.1.2" >nul
if %ERRORLEVEL% neq 0 (
    echo Installing pip 24.1.2...
    python -m pip install --upgrade pip==24.1.2
    if %ERRORLEVEL% neq 0 (
        echo Failed to install pip 24.1.2. Please check your Python installation.
        pause
        exit /b 1
    )
) else (
    echo pip 24.1.2 is already installed.
)

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
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
) else (
    echo Virtual environment activation script not found.
    pause
    exit /b 1
)

:: Install Flask
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                              Installing Flask                              +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install Flask
if %ERRORLEVEL% neq 0 (
    echo Failed to install Flask. Please check your Python installation.
    pause
    exit /b 1
)

:: Install the required dependencies
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                       Installing Required Dependencies                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install dependencies from requirements.txt.
    pause
    exit /b 1
)

:: Upgrade to a specific version of the OpenAI API
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                  Upgrading to a Specific Version of OpenAI API             +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install openai==1.35.15
if %ERRORLEVEL% neq 0 (
    echo Failed to install OpenAI API version 1.35.15.
    pause
    exit /b 1
)

:: Install additional libraries
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                        Install Pillow and requests                         +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install Pillow requests
if %ERRORLEVEL% neq 0 (
    echo Failed to install Pillow and requests.
    pause
    exit /b 1
)

:: Run the Flask application
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                          Running the Flask Application                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
flask run

pause