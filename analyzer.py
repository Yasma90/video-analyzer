"""
Video Analyzer - Transcribe and analyze videos with local AI
Optimized for: 32GB RAM, GPU 8GB, Intel vPro
"""

import whisper
from moviepy import VideoFileClip
import ollama
import torch
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class VideoAnalyzer:
    """Video analyzer with Whisper + Ollama (100% local)"""

    def __init__(self, whisper_model: str = "small", ollama_model: str = "llama2"):
        self.whisper_model_name = whisper_model
        self.ollama_model = ollama_model
        self.whisper_model = None
        self.transcription: str = ""
        self.segments: list = []

        # Detect GPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            print(f"GPU detected: {torch.cuda.get_device_name(0)}")
        else:
            print("Using CPU")

    def _load_whisper(self):
        """Load Whisper model to GPU"""
        if self.whisper_model is None:
            print(f"Loading Whisper ({self.whisper_model_name})...")
            self.whisper_model = whisper.load_model(self.whisper_model_name, device=self.device)
        return self.whisper_model

    def _release_vram(self):
        """Release VRAM for Ollama"""
        self.whisper_model = None
        if self.device == "cuda":
            torch.cuda.empty_cache()

    def transcribe(self, video_path: str, language: str = "es") -> str:
        """Transcribe video to text"""
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        print(f"\nProcessing: {video_path.name}")

        # Extract audio
        print("Extracting audio...")
        audio_path = Path(f"{video_path.stem}_temp_audio.mp3")
        video = VideoFileClip(str(video_path))
        video.audio.write_audiofile(str(audio_path))
        video.close()

        # Transcribe
        print("Transcribing...")
        model = self._load_whisper()
        result = model.transcribe(
            str(audio_path),
            language=language,
            fp16=(self.device == "cuda")
        )

        # Cleanup
        audio_path.unlink()
        self._release_vram()

        self.transcription = result["text"]
        self.segments = result["segments"]

        print("Transcription completed")
        return self.transcription

    def _query_ollama(self, instruction: str) -> str:
        """Query Ollama"""
        response = ollama.chat(
            model=self.ollama_model,
            messages=[{
                "role": "user",
                "content": f"{instruction}\n\nTEXT:\n{self.transcription}"
            }],
            options={"num_ctx": 8192, "num_gpu": 99}
        )
        return response["message"]["content"]

    def summary(self) -> str:
        """Generate executive summary"""
        print("Generating summary...")
        return self._query_ollama(
            "Generate a concise EXECUTIVE SUMMARY in Spanish. "
            "Maximum 3 paragraphs. Capture the essence of the content."
        )

    def key_points(self) -> str:
        """Extract key points"""
        print("Extracting key points...")
        return self._query_ollama(
            "Extract the 8-10 most important KEY POINTS. "
            "Use bullet points. In Spanish. Be concise but informative."
        )

    def detailed_analysis(self) -> str:
        """Complete analysis"""
        print("Generating detailed analysis...")
        return self._query_ollama("""Perform a DETAILED ANALYSIS in Spanish:

## MAIN TOPIC
Describe the central topic of the content.

## MAIN IDEAS
List the most important ideas with brief explanation.

## ARGUMENTS AND DATA
Mention arguments, figures or evidence presented.

## CONCLUSIONS
Summarize conclusions or calls to action.

## AUDIENCE
Who is this content aimed at.""")

    def generate_report(self, video_path: str, output: Optional[str] = None, language: str = "es") -> str:
        """Generate complete report"""
        video_path = Path(video_path)

        # Transcribe
        self.transcribe(video_path, language)

        # Analyze
        print("\nAnalyzing with AI...")
        summary = self.summary()
        points = self.key_points()
        analysis = self.detailed_analysis()

        # Build report
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        report = f"""# VIDEO ANALYSIS

**File:** {video_path.name}
**Date:** {timestamp}
**Models:** Whisper {self.whisper_model_name} + {self.ollama_model}

---

## EXECUTIVE SUMMARY

{summary}

---

## KEY POINTS

{points}

---

## DETAILED ANALYSIS

{analysis}

---

## FULL TRANSCRIPTION

{self.transcription}

---

## TRANSCRIPTION WITH TIMESTAMPS

"""
        for seg in self.segments:
            mins = int(seg['start'] // 60)
            secs = int(seg['start'] % 60)
            report += f"[{mins:02d}:{secs:02d}] {seg['text'].strip()}\n"

        # Save
        if output is None:
            output = video_path.stem + "_analysis.md"

        output_path = Path(output)
        output_path.write_text(report, encoding="utf-8")

        print(f"\nReport saved: {output_path}")
        return report


def main():
    """Main function"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <video.mp4> [language]")
        print("Example: python analyzer.py video.mp4 es")
        sys.exit(1)

    video = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "es"

    analyzer = VideoAnalyzer()
    analyzer.generate_report(video, language=language)


if __name__ == "__main__":
    main()
