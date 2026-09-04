@echo off
cd /d "%~dp0.."

echo ========================================
echo   Video Analyzer - Setup Wizard
echo ========================================
echo.

echo [1/4] Installing Python core dependencies...
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade

echo.
echo [2/4] Installing Ollama (local AI)...
winget install Ollama.Ollama -e --silent

echo.
echo [3/4] Installing FFmpeg...
winget install ffmpeg -e --silent

echo.
echo [4/4] Pulling recommended Ollama model...
ollama pull llama3.1:8b-instruct-q4_0

echo.
echo ========================================
echo   Setup completed successfully!
echo ========================================
echo.
echo Execution options:
echo   - GUI:  scripts\run_gui.bat  or  python gui.py
echo   - CLI:  scripts\run.bat <video.mp4> [en|es]
echo.
pause
