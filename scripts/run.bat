@echo off
cd /d "%~dp0.."

REM Add local FFmpeg to PATH if present
if exist "%~dp0..\ffmpeg-8.0.1-essentials_build\bin" (
    set PATH=%~dp0..\ffmpeg-8.0.1-essentials_build\bin;%PATH%
)

if "%~1"=="" (
    echo Usage: scripts\run.bat <video.mp4> [language]
    echo Example: scripts\run.bat my_video.mp4 en
    pause
    exit /b 1
)

echo Starting Ollama service...
start /B ollama serve >nul 2>&1
timeout /t 3 >nul

echo Processing video...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python analyzer.py %*
pause
