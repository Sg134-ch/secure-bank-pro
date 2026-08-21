@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo Initializing database...
python init_db.py

echo Starting Flask Application...
python app.py
pause
