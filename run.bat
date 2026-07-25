@echo off
REM Bot startup script for Windows
echo Installing dependencies...
pip install -r requirements.txt

echo Starting Discord bot...
python main.py
pause
