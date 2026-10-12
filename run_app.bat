@echo off
setlocal
cd /d "%~dp0"
echo Installing/updating app dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed. Check that Python and pip are installed.
  pause
  exit /b 1
)
echo Starting InfraIntel Streamlit demo...
python -m streamlit run app.py
pause
