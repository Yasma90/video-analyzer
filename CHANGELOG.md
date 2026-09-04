# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-09-04

### Added
- Full Anthropic Claude AI integration supporting Sonnet 4.5, Opus 4.5, 3.5 Sonnet, and 3.5 Haiku.
- Dynamic AI provider selector allowing switching between local Ollama and Cloud Claude API.
- Secure credential management: Claude API keys are input via the UI (held in session memory only, never written to plain-text disk files) with seamless fallback to `ANTHROPIC_API_KEY`.
- Automatic transcription cache recovery system to prevent redundant Whisper re-computations.
- Hardware-assisted Whisper model recommendation engine matching local GPU VRAM.
- Advanced inference controls: token limits and temperature adjustment for both Ollama and Claude.
- Native Drag & Drop support for video file loading.
- Integrated Markdown report previewer directly within the main application window.
- In-app cache and temporary artifact cleanup functionality.
- Senior-level standard repository architecture adopting the Python `src/` layout (`src/video_analyzer`), `tests/`, `scripts/`, and `docs/`.
- Automated test suite in `tests/test_basic.py`.
- Comprehensive English documentation guide ([docs/RECOMMENDED_CONFIGURATION.md](docs/RECOMMENDED_CONFIGURATION.md)).
- Official MIT License attributed to Yasmany Reyes Gonzalez.

### Changed
- Complete modern UI overhaul featuring card-based styling, refined color palettes, and persistent Dark/Light theme toggle.
- Isolated, video-specific temporary audio files preventing naming collisions during concurrent execution.
- Dependency specifications pinned with minimum versions in `requirements.txt` for reliable, reproducible builds.
- Complete type hinting across public API methods in `analyzer.py`.
- Windows automation scripts moved to `scripts/` with relative root resolution and English prompts.

### Fixed
- Fixed bug where Markdown reports showed the Ollama model name even when Claude was the active provider.
- Replaced 9 generic bare `except:` clauses with specific exception handling (`AttributeError`, `OSError`, `RuntimeError`, etc.).
- Removed redundant module-level imports in video processing routines.
- Fixed UI component visibility logic when toggling between AI providers in Settings.

## [0.1.0] - 2024-05-10

### Added
- Initial release featuring OpenAI Whisper speech-to-text and local Ollama model execution.
- Automated audio extraction from video files using MoviePy.
- CLI generation of Markdown summary, key takeaway points, and timestamped transcripts.
