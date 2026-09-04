@echo off
cd /d "%~dp0.."
set PYTHONPATH=src;%PYTHONPATH%

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python -m video_analyzer.gui
pause
