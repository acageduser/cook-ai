@echo off

:: Starting Local Server
echo.
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                               Starting Local Server                        +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.

:: Change to the directory where the script is located
cd /d "%~dp0"

:: Activate the virtual environment
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                        Activating Virtual Environment                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
call venv\Scripts\activate

:: Ensure all dependencies are installed
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                       Installing Required Dependencies                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install -r requirements.txt

:: Run the Flask application
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                          Running the Flask Application                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
flask run
