#!/usr/bin/env python3
"""
GUI entrypoint for Video Analyzer.
Delegates to the src/video_analyzer package.
"""
import sys
from pathlib import Path

# Add src directory to module search path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from video_analyzer.gui import VideoAnalyzerGUI, main

if __name__ == "__main__":
    main()
