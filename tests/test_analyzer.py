"""
Tests for VideoAnalyzer core functionality.
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Ensure mock modules exist in sys.modules so imports succeed in any environment
mock_torch = MagicMock()
mock_torch.cuda.is_available.return_value = False
mock_whisper = MagicMock()
mock_moviepy = MagicMock()
mock_ollama = MagicMock()

for mod_name, mock_obj in [
    ("torch", mock_torch),
    ("whisper", mock_whisper),
    ("moviepy", mock_moviepy),
    ("ollama", mock_ollama),
]:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = mock_obj

from video_analyzer.analyzer import VideoAnalyzer


class TestVideoAnalyzer(unittest.TestCase):
    """Test suite for VideoAnalyzer CLI and core processing engine."""

    def setUp(self):
        self.analyzer = VideoAnalyzer(whisper_model="base", ollama_model="llama3")

    def test_init_defaults(self):
        """Test default initialization values."""
        default_analyzer = VideoAnalyzer()
        self.assertEqual(default_analyzer.whisper_model_name, "small")
        self.assertEqual(default_analyzer.ollama_model, "llama2")
        self.assertEqual(default_analyzer.transcription, "")
        self.assertEqual(default_analyzer.segments, [])
        self.assertIn(default_analyzer.device, ["cuda", "cpu"])

    def test_init_custom_parameters(self):
        """Test custom initialization parameters."""
        self.assertEqual(self.analyzer.whisper_model_name, "base")
        self.assertEqual(self.analyzer.ollama_model, "llama3")

    def test_transcribe_file_not_found(self):
        """Test that transcribe raises FileNotFoundError for non-existent video."""
        with self.assertRaises(FileNotFoundError):
            self.analyzer.transcribe("non_existent_video_12345.mp4")

    def test_transcribe_success(self):
        """Test successful video transcription workflow with mocked dependencies."""
        mock_clip_instance = MagicMock()
        mock_moviepy.VideoFileClip.return_value = mock_clip_instance

        mock_whisper_instance = MagicMock()
        mock_whisper_instance.transcribe.return_value = {
            "text": "This is a test transcript.",
            "segments": [
                {"start": 0.0, "end": 2.5, "text": "This is a"},
                {"start": 2.5, "end": 5.0, "text": "test transcript."}
            ]
        }
        mock_whisper.load_model.return_value = mock_whisper_instance

        dummy_video = Path("test_dummy_video.mp4")
        dummy_video.touch()

        try:
            with patch.object(Path, "unlink", return_value=None):
                result = self.analyzer.transcribe(str(dummy_video), language="en")

            self.assertEqual(result, "This is a test transcript.")
            self.assertEqual(self.analyzer.transcription, "This is a test transcript.")
            self.assertEqual(len(self.analyzer.segments), 2)
            mock_clip_instance.audio.write_audiofile.assert_called_once()
            mock_clip_instance.close.assert_called_once()
        finally:
            if dummy_video.exists():
                dummy_video.unlink()

    def test_query_ollama(self):
        """Test Ollama querying method with instructions."""
        mock_ollama.chat.return_value = {
            "message": {"content": "Generated summary from local AI."}
        }
        self.analyzer.transcription = "Video transcript sample."
        result = self.analyzer._query_ollama("Summarize this video")

        self.assertEqual(result, "Generated summary from local AI.")
        mock_ollama.chat.assert_called_once()
        call_kwargs = mock_ollama.chat.call_args[1]
        self.assertEqual(call_kwargs["model"], "llama3")
        self.assertIn("Summarize this video", call_kwargs["messages"][0]["content"])
        self.assertIn("Video transcript sample.", call_kwargs["messages"][0]["content"])

    @patch.object(VideoAnalyzer, "_query_ollama")
    def test_summary_and_key_points(self, mock_query):
        """Test summary, key_points, and detailed_analysis helper methods."""
        mock_query.return_value = "Mocked AI Response"

        self.assertEqual(self.analyzer.summary(), "Mocked AI Response")
        self.assertEqual(self.analyzer.key_points(), "Mocked AI Response")
        self.assertEqual(self.analyzer.detailed_analysis(), "Mocked AI Response")
        self.assertEqual(mock_query.call_count, 3)

    @patch.object(VideoAnalyzer, "transcribe")
    @patch.object(VideoAnalyzer, "summary")
    @patch.object(VideoAnalyzer, "key_points")
    @patch.object(VideoAnalyzer, "detailed_analysis")
    def test_generate_report(self, mock_details, mock_points, mock_summary, mock_transcribe):
        """Test generate_report output formatting and file saving."""
        mock_summary.return_value = "Executive summary text."
        mock_points.return_value = "- Key takeaway 1\n- Key takeaway 2"
        mock_details.return_value = "Deep analytical breakdown."

        self.analyzer.transcription = "Full transcript."
        self.analyzer.segments = [
            {"start": 15.0, "text": "Segment at 15 seconds"},
            {"start": 75.0, "text": "Segment at 1 minute 15 seconds"},
        ]

        dummy_video = Path("sample_presentation.mp4")
        dummy_video.touch()
        output_report = Path("test_output_report.md")

        try:
            report = self.analyzer.generate_report(
                str(dummy_video),
                output=str(output_report),
                language="en"
            )

            self.assertIn("# VIDEO ANALYSIS", report)
            self.assertIn("Executive summary text.", report)
            self.assertIn("- Key takeaway 1", report)
            self.assertIn("[00:15] Segment at 15 seconds", report)
            self.assertIn("[01:15] Segment at 1 minute 15 seconds", report)
            self.assertTrue(output_report.exists())
            self.assertEqual(output_report.read_text(encoding="utf-8"), report)
        finally:
            if dummy_video.exists():
                dummy_video.unlink()
            if output_report.exists():
                output_report.unlink()


if __name__ == "__main__":
    unittest.main()
