@echo off
setlocal

:: Function to check for errors after commands
:check_error
if %ERRORLEVEL% neq 0 (
    echo ERROR: An error occurred. Please check the previous command.
    pause
    exit /b 1
)
goto :eof

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
call :check_error

:: Activate the virtual environment
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                         Activating Virtual Environment                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
    echo Virtual environment activated.
) else (
    echo ERROR: Virtual environment activation script not found.
    pause
    exit /b 1
)
call :check_error

:: Install Flask
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                              Installing Flask                              +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
pip install Flask
call :check_error

:: Install the required dependencies
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                       Installing Required Dependencies                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
if exist "requirements.txt" (
    pip install -r requirements.txt
    call :check_error
) else (
    echo ERROR: requirements.txt not found.
    pause
    exit /b 1
)

:: Run the Flask application
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +                          Running the Flask Application                     +
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.
flask run
call :check_error

pause
