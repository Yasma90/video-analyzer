@echo off
cd /d "%~dp0.."

REM Add FFmpeg to PATH if present locally
if exist "%~dp0..\ffmpeg-8.0.1-essentials_build\bin" (
    set PATH=%~dp0..\ffmpeg-8.0.1-essentials_build\bin;%PATH%
)

if "%~1"=="" (
    echo Uso: run.bat video.mp4 [idioma]
    echo Ejemplo: run.bat my_video.mp4 es
    pause
    exit /b 1
)

echo Iniciando Ollama...
start /B ollama serve >nul 2>&1
timeout /t 3 >nul

echo Procesando video...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python analyzer.py %*
pause
