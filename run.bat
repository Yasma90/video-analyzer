@echo off
cd /d "%~dp0"

REM Add FFmpeg to PATH
set PATH=%~dp0ffmpeg-8.0.1-essentials_build\bin;%PATH%

if "%~1"=="" (
    echo Usage: run.bat video.mp4 [language]
    echo Example: run.bat my_video.mp4 es
    pause
    exit /b 1
)

echo Starting Ollama...
start /B ollama serve >nul 2>&1
timeout /t 3 >nul

echo Processing video...
call venv\Scripts\activate
python analyzer.py %*
pause
