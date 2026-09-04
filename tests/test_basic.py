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

    def test_package_structure_exists(self):
        """Verify strict src-layout structure without loose files in root."""
        root = Path(__file__).resolve().parent.parent
        self.assertTrue((root / "src" / "video_analyzer" / "__init__.py").exists())
        self.assertTrue((root / "src" / "video_analyzer" / "analyzer.py").exists())
        self.assertTrue((root / "src" / "video_analyzer" / "gui.py").exists())
        self.assertTrue((root / "requirements.txt").exists())
        self.assertTrue((root / "CHANGELOG.md").exists())
        self.assertTrue((root / "LICENSE").exists())
        self.assertTrue((root / "README.md").exists())
        self.assertTrue((root / "scripts" / "run.bat").exists())
        self.assertTrue((root / "scripts" / "run_gui.bat").exists())
        self.assertTrue((root / "scripts" / "setup.bat").exists())
        # Ensure no loose python scripts in project root
        self.assertFalse((root / "analyzer.py").exists())
        self.assertFalse((root / "gui.py").exists())


if __name__ == "__main__":
    unittest.main()
