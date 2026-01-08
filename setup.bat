@echo off
echo ========================================
echo   Video Analyzer - Setup
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt --index-url https://download.pytorch.org/whl/cu121

echo.
echo [2/4] Installing Ollama...
winget install Ollama.Ollama -e --silent

echo.
echo [3/4] Installing FFmpeg...
winget install ffmpeg -e --silent

echo.
echo [4/4] Downloading Ollama model...
ollama pull llama3.1:8b-instruct-q4_0

echo.
echo ========================================
echo   Setup completed!
echo ========================================
echo.
echo Usage:
echo   python analyzer.py video.mp4
echo   python gui.py  (for GUI)
echo.
pause
