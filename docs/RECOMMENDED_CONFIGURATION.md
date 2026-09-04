# Recommended Configuration Guide - Video Analyzer v1.0.0

This guide helps you choose the optimal configuration based on your hardware resources and quality requirements.

---

## 🖥️ Configuration by Hardware Profile

### NVIDIA GPU with 10GB+ VRAM (RTX 3080, RTX 4090, A6000)
**Maximum Performance & Fidelity**

```ini
Whisper Model: large
AI Provider: Ollama (local) or Claude (highest reasoning quality)
Ollama Model: llama3.1:70b or mixtral:8x7b
Claude Model: claude-opus-4-5-20251101
GPU Acceleration: Enabled (CUDA)
Context Window: 16384
Temperature: 0.5 - 0.7
```

- **Speed:** ~5-8 minutes per hour of video
- **Quality:** Superior / Academic & Legal grade
- **Cost:** Free (Ollama) / Pay-as-you-go (Claude Opus)

---

### NVIDIA GPU with 6-10GB VRAM (RTX 3060, RTX 4060, A4000)
**Optimal Balance (⭐ Recommended for Most Users)**

```ini
Whisper Model: medium
AI Provider: Claude or Ollama
Ollama Model: llama3.1:8b or mistral
Claude Model: claude-sonnet-4-5-20250929
GPU Acceleration: Enabled (CUDA)
Context Window: 8192
Temperature: 0.5 - 0.7
```

- **Speed:** ~3-5 minutes per hour of video
- **Quality:** Very High
- **Cost:** Free (Ollama) / Very Low (Claude Sonnet)

---

### NVIDIA GPU with 4-6GB VRAM (GTX 1660, RTX 3050, RTX A500)
**Standard Acceleration**

```ini
Whisper Model: small
AI Provider: Ollama
Ollama Model: llama3.1:8b or llama2
GPU Acceleration: Enabled (CUDA)
Context Window: 8192
Temperature: 0.7
```

- **Speed:** ~2-3 minutes per hour of video
- **Quality:** High
- **Cost:** Free

---

### CPU / GPU with < 4GB VRAM
**Resource-Efficient Mode**

```ini
Whisper Model: base or tiny
AI Provider: Claude (recommended) or Ollama
Ollama Model: llama2
Claude Model: claude-3-5-haiku-20241022
GPU Acceleration: Disabled
Context Window: 4096
Temperature: 0.7
```

- **Speed:** ~10-20 minutes per hour of video (CPU execution)
- **Quality:** Good / Acceptable
- **Cost:** Free (Ollama) / Extremely economical (Claude Haiku)

---

## 🎯 Configuration by Goal

### 1. High-Accuracy Professional Summaries
- **Whisper Model:** `large` or `medium`
- **AI Provider:** Claude (`claude-sonnet-4-5-20250929` or `claude-opus-4-5-20251101`)
- **Temperature:** `0.3` (deterministic and structured)
- **Output Format:** Markdown (`.md`)
- **Best for:** Technical presentations, legal depositions, academic lectures.

### 2. High-Throughput Batch Processing
- **Whisper Model:** `base` or `tiny`
- **AI Provider:** Ollama (`llama2` or `mistral`)
- **Temperature:** `0.7`
- **Delete Temp Audio:** Enabled
- **Best for:** Fast triage, bulk video cataloging, drafts.

### 3. Code & Technical Tutorials
- **Whisper Model:** `medium` or `large`
- **AI Provider:** Claude (`claude-sonnet-4-5-20250929`)
- **Max Tokens:** `4096`
- **Temperature:** `0.2`
- **Best for:** Engineering workshops, programming tutorials, system walkthroughs.

---

## 📝 Advanced Parameter Details

### Temperature (`0.0 - 1.0`)
Controls the randomness of AI responses:
- `0.0 - 0.3`: Precise, conservative, and deterministic. Best for technical and factual summaries.
- `0.4 - 0.7`: Balanced creativity and precision. Default recommended setting.
- `0.8 - 1.0`: Creative and expressive. Useful for brainstorming and open-ended narrative generation.

### Context Window (Ollama Only)
Controls token retention for local models:
- `4096`: Minimal, suited for short clips (< 15 mins).
- `8192`: Standard, suited for medium videos (15-45 mins).
- `16384`: Extended, suited for long recordings (> 45 mins).

### Max Tokens (Claude Only)
Controls maximum generation length per section:
- `2048`: Concise summaries.
- `4096`: Comprehensive and detailed reports (Default).
- `8192`: Deeply granular breakdown.

---

## 💡 Performance and Cost Optimization Tips

1. **VRAM Safety:**
   If you experience CUDA out-of-memory errors:
   - Step down one Whisper model tier (e.g., `medium` → `small`).
   - Lower the Ollama context window size.
   - Close other VRAM-heavy applications (browsers, 3D software).

2. **Cost Management with Claude:**
   - Use Ollama for preliminary transcription checks.
   - Use `claude-3-5-haiku` for cost-sensitive standard jobs.
   - Restrict `claude-opus` to high-stakes executive or publication reports.
   - Credentials are held in session memory or resolved from `ANTHROPIC_API_KEY` to guarantee security.

---

## 📊 Model Comparison Matrix

### Ollama Models (Local, Offline & Free)

| Model | Memory Footprint | Inference Speed | Quality | Multilingual Support |
|---|---|---|---|---|
| `llama2` | ~4GB VRAM | Fast | Good | Moderate |
| `llama3.1:8b` | ~6GB VRAM | Medium | Very High | Excellent |
| `mistral` | ~5GB VRAM | Fast | Very High | Excellent |
| `llama3.1:70b` | ~40GB VRAM | Slow | Superior | State-of-the-Art |

### Anthropic Claude Models (Cloud API)

| Model | Speed | Quality | Pricing Tier | Best Use Case |
|---|---|---|---|---|
| `claude-3-5-haiku` | Very Fast | High | Ultra Low | Rapid summaries, cost efficiency |
| `claude-3-5-sonnet` | Fast | Superior | Moderate | High quality balance |
| `claude-sonnet-4-5` | Fast | Superior | Moderate | Complex reasoning, detailed notes |
| `claude-opus-4-5` | Medium | Maximum | Premium | Critical documents, zero-defect analysis |

---

## ❓ Frequently Asked Questions (FAQ)

**Q: Where is my configuration stored?**  
A: Preferences persist locally in `config.json` at the repository root. Sensitive API keys are never persisted in plain text to disk.

**Q: Can I run completely offline without internet?**  
A: Yes! Use OpenAI Whisper + Ollama with pre-downloaded models for a 100% offline, private workflow.
