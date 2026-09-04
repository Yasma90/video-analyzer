@echo off
cd /d "%~dp0.."

echo ========================================
echo   Video Analyzer - Setup
echo ========================================
echo.

echo [1/4] Instalando dependencias de Python...
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade

echo.
echo [2/4] Instalando Ollama...
winget install Ollama.Ollama -e --silent

echo.
echo [3/4] Instalando FFmpeg...
winget install ffmpeg -e --silent

echo.
echo [4/4] Descargando modelo Ollama recomendado...
ollama pull llama3.1:8b-instruct-q4_0

echo.
echo ========================================
echo   Instalacion completada con exito!
echo ========================================
echo.
echo Modos de ejecucion:
echo   - GUI:    scripts\run_gui.bat  o  python gui.py
echo   - CLI:    scripts\run.bat tu_video.mp4 [es|en]
echo.
pause
