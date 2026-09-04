"""
Tests for VideoAnalyzer GUI and application logic functions.
"""
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Import or register mock modules in sys.modules
for mod in ["torch", "ollama", "anthropic", "whisper", "moviepy"]:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

import torch
import ollama
import anthropic

from video_analyzer.gui import (
    DEFAULT_CONFIG,
    VideoAnalyzerGUI,
    format_time,
    get_ollama_models,
    get_recommended_config,
    load_config,
    save_config,
)


class TestGUILogic(unittest.TestCase):
    """Test suite for GUI logic, hardware detection, caching, and AI providers."""

    def test_format_time(self):
        """Test formatting seconds to MM:SS."""
        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(59), "00:59")
        self.assertEqual(format_time(60), "01:00")
        self.assertEqual(format_time(125), "02:05")
        self.assertEqual(format_time(3661), "61:01")

    def test_get_recommended_config_cuda_tiers(self):
        """Test automatic Whisper model selection based on VRAM tiers."""
        torch.cuda.is_available.return_value = True

        # Tier 1: >= 10GB -> large
        torch.cuda.get_device_properties.return_value = MagicMock(total_memory=11 * (1024**3))
        cfg = get_recommended_config()
        self.assertEqual(cfg["whisper_model"], "large")
        self.assertTrue(cfg["use_gpu"])

        # Tier 2: >= 5GB -> medium
        torch.cuda.get_device_properties.return_value = MagicMock(total_memory=6 * (1024**3))
        cfg = get_recommended_config()
        self.assertEqual(cfg["whisper_model"], "medium")

        # Tier 3: >= 2GB -> small
        torch.cuda.get_device_properties.return_value = MagicMock(total_memory=3 * (1024**3))
        cfg = get_recommended_config()
        self.assertEqual(cfg["whisper_model"], "small")

        # Tier 4: >= 1GB -> base
        torch.cuda.get_device_properties.return_value = MagicMock(total_memory=1.5 * (1024**3))
        cfg = get_recommended_config()
        self.assertEqual(cfg["whisper_model"], "base")

        # Tier 5: < 1GB -> tiny
        torch.cuda.get_device_properties.return_value = MagicMock(total_memory=0.8 * (1024**3))
        cfg = get_recommended_config()
        self.assertEqual(cfg["whisper_model"], "tiny")

    def test_get_recommended_config_cpu(self):
        """Test CPU fallback when CUDA is not available."""
        torch.cuda.is_available.return_value = False
        cfg = get_recommended_config()
        self.assertEqual(cfg["whisper_model"], "base")
        self.assertFalse(cfg["use_gpu"])

    def test_save_config_strips_api_key(self):
        """Verify save_config never persists plain-text API keys to disk."""
        test_cfg_path = Path("test_config_safety.json")
        sample_config = DEFAULT_CONFIG.copy()
        sample_config["claude_api_key"] = "sk-ant-secret-key-that-must-never-be-saved"
        sample_config["theme"] = "light"

        try:
            with patch("video_analyzer.gui.CONFIG_FILE", test_cfg_path):
                save_config(sample_config)
                self.assertTrue(test_cfg_path.exists())

                with open(test_cfg_path, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)

                # The key must be stripped to an empty string on disk
                self.assertEqual(saved_data["claude_api_key"], "")
                self.assertEqual(saved_data["theme"], "light")
        finally:
            if test_cfg_path.exists():
                test_cfg_path.unlink()

    def test_load_config_existing_and_default(self):
        """Test load_config reads existing JSON values and applies defaults."""
        test_cfg_path = Path("test_load_config.json")
        custom_data = {"theme": "light", "ollama_model": "codellama"}

        try:
            with open(test_cfg_path, "w", encoding="utf-8") as f:
                json.dump(custom_data, f)

            with patch("video_analyzer.gui.CONFIG_FILE", test_cfg_path):
                loaded = load_config()
                self.assertEqual(loaded["theme"], "light")
                self.assertEqual(loaded["ollama_model"], "codellama")
                # Defaults preserved
                self.assertEqual(loaded["language"], "es")
        finally:
            if test_cfg_path.exists():
                test_cfg_path.unlink()

    def test_get_ollama_models_success(self):
        """Test retrieving installed Ollama models."""
        ollama.list.return_value = {
            "models": [{"name": "llama3.1:latest"}, {"name": "mistral:7b"}]
        }
        ollama.list.side_effect = None
        models = get_ollama_models()
        self.assertIn("llama3.1", models)
        self.assertIn("mistral", models)

    def test_get_ollama_models_fallback(self):
        """Test fallback models list when Ollama server is offline."""
        ollama.list.side_effect = Exception("Connection refused")
        models = get_ollama_models()
        self.assertIn("llama2", models)
        self.assertIn("mistral", models)
        ollama.list.side_effect = None


class TestGUIAppLogic(unittest.TestCase):
    """Test suite for VideoAnalyzerGUI internal worker methods."""

    def setUp(self):
        # Instantiate a minimal mock harness for VideoAnalyzerGUI methods
        self.gui = VideoAnalyzerGUI.__new__(VideoAnalyzerGUI)
        self.gui.config = DEFAULT_CONFIG.copy()
        ollama.chat.reset_mock()
        anthropic.Anthropic.reset_mock()

    def test_cache_file_paths_and_operations(self):
        """Test cache file creation, loading, and deletion."""
        video_path = Path("test_video_sample.mp4")
        cache_file = video_path.parent / f"{video_path.stem}_cache.json"

        sample_data = {
            "transcription": "Cached hello world",
            "segments": [{"start": 0.0, "end": 2.0, "text": "Cached hello"}],
            "duration": 2.0,
        }

        try:
            # Save cache manually as gui does
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(sample_data, f)
            self.assertTrue(cache_file.exists())

            # Verify reading cache data
            with open(cache_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            self.assertEqual(loaded["transcription"], "Cached hello world")
            self.assertEqual(len(loaded["segments"]), 1)

            # Test cache deletion
            cache_file.unlink()
            self.assertFalse(cache_file.exists())
        finally:
            if cache_file.exists():
                cache_file.unlink()

    def test_query_claude_missing_key_raises_error(self):
        """Test that _query_claude raises ValueError if no key is configured and none in env."""
        self.gui.config["claude_api_key"] = ""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}):
            with self.assertRaises(ValueError) as ctx:
                self.gui._query_claude("Test prompt", "Sample text")
            self.assertIn("API Key de Claude no configurada", str(ctx.exception))

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-from-env"})
    def test_query_claude_with_env_key(self):
        """Test that _query_claude picks up ANTHROPIC_API_KEY from environment."""
        self.gui.config["claude_api_key"] = ""
        mock_client = MagicMock()
        anthropic.Anthropic.return_value = mock_client

        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="Claude response generated")]
        mock_client.messages.create.return_value = mock_msg

        response = self.gui._query_claude("Summarize", "Content")
        self.assertEqual(response, "Claude response generated")
        anthropic.Anthropic.assert_called_with(api_key="sk-ant-test-from-env")

    def test_query_ollama(self):
        """Test _query_ollama passes correct options and receives text."""
        self.gui.config["ollama_model"] = "llama3"
        self.gui.config["ollama_ctx"] = 4096
        self.gui.config["ollama_temp"] = 0.6

        ollama.chat.return_value = {
            "message": {"content": "Ollama response generated"}
        }

        result = self.gui._query_ollama("Analyze", "Video text")
        self.assertEqual(result, "Ollama response generated")
        ollama.chat.assert_called_once()
        kwargs = ollama.chat.call_args[1]
        self.assertEqual(kwargs["options"]["num_ctx"], 4096)
        self.assertEqual(kwargs["options"]["temperature"], 0.6)

    def test_query_ai_routing(self):
        """Test _query_ai routes dynamically between Ollama and Claude."""
        with patch.object(self.gui, "_query_ollama", return_value="From Ollama") as mock_ollama_method:
            with patch.object(self.gui, "_query_claude", return_value="From Claude") as mock_claude_method:
                self.gui.config["ai_provider"] = "ollama"
                self.assertEqual(self.gui._query_ai("prompt", "text"), "From Ollama")
                mock_ollama_method.assert_called_once()

                self.gui.config["ai_provider"] = "claude"
                self.assertEqual(self.gui._query_ai("prompt", "text"), "From Claude")
                mock_claude_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
