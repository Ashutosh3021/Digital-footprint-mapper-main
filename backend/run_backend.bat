@echo off
echo Starting DFM OSINT Backend...
echo Make sure you have Python and the required packages installed.
echo Installing dependencies...
pip install -r requirements.txt
echo Starting server on http://localhost:8004
uvicorn main:app --host 0.0.0.0 --port 8004 --reload
pause