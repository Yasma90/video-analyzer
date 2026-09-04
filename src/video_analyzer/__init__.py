"""
Video Analyzer Package
Transcribe and analyze videos using local AI (Whisper + Ollama) or Cloud AI (Anthropic Claude).
"""

__version__ = "1.0.0"
__author__ = "Yasmany Reyes Gonzalez"
__license__ = "MIT"

try:
    from .analyzer import VideoAnalyzer
except ImportError:
    VideoAnalyzer = None

__all__ = ["VideoAnalyzer", "__version__"]
