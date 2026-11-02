@echo off
REM Setup script for MLDS Week 1 project (Windows)
REM Creates virtual environment and installs dependencies

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete! Virtual environment is activated.
echo To activate it later, run: venv\Scripts\activate
