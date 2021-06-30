@ECHO OFF
ECHO Activating virtual environment

CALL venv\Scripts\activate.bat

ECHO Building Package

pyinstaller --additional-hooks-dir=pyinstaller-hooks --onefile --add-data "app/icon.png;./app" --icon "app/icon.ico" --noconsole --name="SUH" main.py
