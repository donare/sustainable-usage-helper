@ECHO OFF
ECHO Activating virtual environment

CALL venv\Scripts\activate.bat

ECHO Building Package

pyinstaller --additional-hooks-dir=pyinstaller-hooks --onefile --add-data "icon.png;." --icon "icon.ico" --noconsole --name="SUH" main.py
