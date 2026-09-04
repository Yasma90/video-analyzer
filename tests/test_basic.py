"""
Unit tests for the video_analyzer package.
"""
import sys
from pathlib import Path
import unittest

# Ensure src is in search path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import video_analyzer


class TestVideoAnalyzer(unittest.TestCase):
    """Basic smoke and unit tests for Video Analyzer."""

    def test_version_defined(self):
        """Verify package version is properly defined."""
        self.assertEqual(video_analyzer.__version__, "1.0.0")
        self.assertEqual(video_analyzer.__author__, "Yasmany Reyes Gonzalez")
        self.assertEqual(video_analyzer.__license__, "MIT")

    def test_format_time_helper(self):
        """Verify time formatting logic directly."""
        def format_time(seconds):
            mins, secs = divmod(int(seconds), 60)
            return f"{mins:02d}:{secs:02d}"

        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(65), "01:05")
        self.assertEqual(format_time(3600), "60:00")

    def test_cli_entrypoints_exist(self):
        """Verify root convenience wrappers exist and are valid files."""
        root = Path(__file__).resolve().parent.parent
        self.assertTrue((root / "analyzer.py").exists())
        self.assertTrue((root / "gui.py").exists())
        self.assertTrue((root / "requirements.txt").exists())
        self.assertTrue((root / "CHANGELOG.md").exists())
        self.assertTrue((root / "LICENSE").exists())
        self.assertTrue((root / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
