# Video Analyzer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Release-v1.0.0-green.svg)](CHANGELOG.md)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

**Video Analyzer** is an AI-powered desktop and command-line application that transcribes video files into text and generates comprehensive executive summaries, key takeaway points, and structured analyses. It supports **100% offline, private execution** via [OpenAI Whisper](https://github.com/openai/whisper) and [Ollama](https://ollama.com), as well as cloud-powered high-reasoning intelligence via [Anthropic Claude AI](https://anthropic.com).

---

## ✨ Features

- **🎙️ Automatic Speech-to-Text**: High-accuracy multi-lingual transcription powered by OpenAI Whisper (from `tiny` to `large`).
- **🤖 Dual AI Inference Engine**:
  - **Local & Private**: Run open-source LLMs locally via Ollama (`llama3.1`, `mistral`, `codellama`).
  - **Cloud Reasoning**: Leverage Anthropic Claude (`Sonnet 4.5`, `Opus 4.5`, `3.5 Sonnet`, `3.5 Haiku`).
- **🔐 Secure Credential Management**:
  - Claude API keys are input interactively through the UI and stored strictly in session memory.
  - No sensitive keys or tokens are ever committed or persisted in plain-text disk files.
  - Full support for the `ANTHROPIC_API_KEY` environment variable.
- **⚡ Smart Transcription Cache**: Automatically caches transcriptions to avoid redundant processing when iterating on analysis prompts.
- **🖥️ Hardware Acceleration & Auto-Detection**: Detects available NVIDIA GPU VRAM to recommend optimal Whisper model configurations.
- **🎨 Modern Desktop UI**:
  - Built with responsive card-based architecture.
  - Native **Dark** and **Light** themes with instant toggling and persistence.
  - Built-in Markdown report viewer.
  - Native **Drag & Drop** support for video files.
- **📦 Clean Architecture**: Senior-grade project structure following the modern Python `src/` layout with unit test coverage and modular scripts.

---

## 🏗️ Repository Architecture

```text
video-analyzer/
├── docs/                               # Detailed technical guides and references
│   └── RECOMMENDED_CONFIGURATION.md   # Hardware benchmarks, VRAM sizing, and model selection
├── scripts/                            # Automation scripts
│   ├── run.bat                         # Windows CLI launcher
│   ├── run_gui.bat                     # Windows desktop GUI launcher
│   └── setup.bat                       # Automated setup and dependencies installer
├── src/                                # Core package source code (src-layout)
│   └── video_analyzer/
│       ├── __init__.py                 # Package metadata and public exports
│       ├── analyzer.py                 # Core video transcription & report engine
│       └── gui.py                      # Modern Tkinter graphical user interface
├── tests/                              # Automated test suite
│   ├── __init__.py
│   └── test_basic.py                   # Smoke tests and core validations
├── .gitignore                          # Strict ignore rules for temp files, cache, and venv
├── analyzer.py                         # Root convenience CLI entrypoint
├── CHANGELOG.md                        # Version release history (Keep a Changelog standard)
├── gui.py                              # Root convenience GUI entrypoint
├── LICENSE                             # MIT License (Yasmany Reyes Gonzalez)
├── README.md                           # Project documentation
└── requirements.txt                    # Pinned core dependencies
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- **Python 3.10+**
- **NVIDIA GPU** with CUDA support recommended (CPU is supported as a fallback)
- **FFmpeg** (included or installed via system package manager)
- **Ollama** (optional, for local offline AI)

### 1. Clone the Repository
```bash
git clone https://github.com/Yasma90/video-analyzer.git
cd video-analyzer
```

### 2. Environment Setup
Create and activate a virtual environment:
```bash
python -m venv venv

# Windows (Command Prompt / PowerShell)
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

For NVIDIA GPU acceleration with PyTorch CUDA:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade
```

Or run the automated setup wizard on Windows:
```bash
scripts\setup.bat
```

---

## 💻 Usage

### Desktop GUI (Recommended)
Launch the graphical interface:

```bash
# Option 1: Convenience script
scripts\run_gui.bat

# Option 2: Direct execution
python gui.py
```

### Command Line Interface (CLI)
Process videos directly from your terminal:

```bash
# Option 1: Convenience batch script (Windows)
scripts\run.bat "path\to\video.mp4" [language_code]

# Option 2: Direct CLI execution
python analyzer.py "path\to\video.mp4" es
```

---

## 🔒 API Key & Credential Safety

When utilizing Anthropic Claude AI:
1. **Interactive Prompt**: If no API key is detected upon starting an analysis, the application opens a secure modal prompt (`show='*'`) to receive your key.
2. **In-Memory Only**: Keys provided through the UI are retained exclusively in volatile memory for the active session. They are **never** written into `config.json` or any tracked file.
3. **Environment Variable**: Alternatively, export `ANTHROPIC_API_KEY`:
   ```bash
   # Windows PowerShell
   $env:ANTHROPIC_API_KEY="sk-ant-..."

   # Linux / macOS
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

---

## 🧪 Running Tests

Execute the automated test suite with standard `unittest`:

```bash
python -m unittest discover tests
```

---

## 📖 Configuration & Hardware Tuning

For in-depth hardware profiles, VRAM requirements, and performance tips, refer to the [Recommended Configuration Guide](docs/RECOMMENDED_CONFIGURATION.md).

| Whisper Model | VRAM Required | Precision | Speed |
|---|---|---|---|
| `tiny` | ~1 GB | Basic | Fastest |
| `base` | ~1 GB | Acceptable | Fast |
| `small` | ~2 GB | Good (Balanced) | Moderate |
| `medium` | ~5 GB | Very High | Slower |
| `large` | ~10 GB | State-of-the-Art | Intensive |

---

## 📄 Output Formats

Analyses are saved alongside the video or in your configured output folder:
- **Markdown (`.md`)**: Full report with executive summary, bullet points, and timestamped transcript.
- **JSON (`.json`)**: Structured dictionary including segments, metadata, and analytical sections.
- **Text (`.txt`)**: Plain-text clean output.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024-2026 **Yasmany Reyes Gonzalez**.
