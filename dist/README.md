How to Build the CookAI Executable:

Important: Do NOT run CMD as an Administrator! PyInstaller will fail in Admin mode.

Steps:

1. Open CMD and `cd` into the `cookAI` folder (make sure you're not in Admin mode).

   cd path\to\cookAI

2. Activate the virtual environment (venv):

   On Windows, use:
   
   venv\Scripts\activate

3. Run the following PyInstaller command to package the app:

   pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --name cookai --icon static/img/cook-ai-favicon.ico --specpath ./ app.py

This will generate a standalone executable with the custom icon from static/img/aook-ai-favicon.ico.


Notes ~
1. You might have to install some things while the virtual environment is running, and other times while it's not running.