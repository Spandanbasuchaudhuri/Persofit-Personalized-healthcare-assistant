# 🤖 Multimodal AI Assistant

A **Streamlit-powered** personal assistant that fuses conversational AI, voice synthesis, health recommendations, reminder scheduling, and on-device OCR—all runnable **offline** via [Ollama](https://ollama.ai).  
Think of it as a local “Jarvis” that chats, speaks, plans your workouts, reminds you to hydrate, and even reads receipts or PDFs.

---

## 📋 Table of Contents
1. [Project Vision](#-project-vision)  
2. [Feature Matrix](#-feature-matrix)  
3. [Architecture](#-architecture)  
4. [Demo Screens](#-demo-screens)  
5. [Quick Start](#-quick-start)  
6. [Configuration](#-configuration)  
7. [Usage Guide](#-usage-guide)  
8. [Extending the Assistant](#-extending-the-assistant)  
9. [Project Layout](#-project-layout)  
10. [Troubleshooting](#-troubleshooting)  
11. [Roadmap](#-roadmap)  
12. [Contributing](#-contributing)  
13. [License & Credits](#-license--credits)

---

## 🎯 Project Vision
> **Goal:** Provide an offline-first template that demonstrates how to braid **LLMs**, **text-to-speech (TTS)**, **OCR**, and **simple scheduling** into a cohesive Streamlit experience.  
> **Audience:** Students and hobbyists exploring AI integration without cloud fees or vendor lock-in.  
> **Philosophy:** *Local-first*, *hack-friendly*, and *model-agnostic*—swap any Ollama model with a single line of code.

---

## ✨ Feature Matrix

| Module | Capability | Tech Stack | Key File(s) |
|--------|------------|------------|-------------|
| **Chat Interface** | 🔹 Real-time streaming chat<br>🔹 Markdown-aware rendering | Streamlit UI + `ollama.chat()` | `main.py` (UI), `ai_response.py` |
| **Voice Output** | 🔹 8 Edge-TTS voices<br>🔹 Toggle per-message | Microsoft Edge TTS | `audio_output.py` |
| **Diet Planner** | 🔹 Balanced macronutrient breakdown<br>🔹 Meal-by-meal suggestions | LLM prompt + validation schema | `diet.py` |
| **Workout Planner** | 🔹 Beginner → pro routines<br>🔹 Progressive-overload logic | LLM prompt w/ load table | `exercise.py` |
| **Smart Reminders** | 🔹 In-browser toast + sound<br>🔹 Runs *client-side* every minute | Streamlit JS hack | `reminders.py` |
| **OCR & PDF Parsing** | 🔹 Image → text via Tesseract<br>🔹 PDF page text with PyPDF2 | `pytesseract`, `pypdf2` | `file_processing.py` |

---

## 🏗 Architecture
```text
┌────────────┐       user query/params        ┌──────────────┐
│ Streamlit  │ ─────────────────────────────▶ │  ai_response │
│   front-end│ ◀──────── Markdown + audio ─── │   module     │
└────────────┘                                 └─────┬────────┘
       ▲                                             │
       │     image/PDF                               ▼
┌──────┴──────┐                              ┌──────────────┐
│ file_upload │ ──▶ OCR via Tesseract ──────▶│file_processing│
└─────────────┘                              └──────────────┘
       ▲                                             ▲
       │ reminders                                   │
┌──────┴──────┐                              ┌──────────────┐
│ reminders   │ ◀──────── toast/JS ───────── │  browser tab │
└─────────────┘                              └──────────────┘
````

*All heavy lifting—LLM inference and TTS—happens locally; only a lightweight WebSocket serves Streamlit.*

---

## 🖼 Demo Screens

> *(GIF / screenshots placeholder – drop into `/assets` once recorded)*

---

## 🚀 Quick Start

### 1. Clone & Activate Env

```bash
git clone https://github.com/<you>/multimodal-ai-assistant.git
cd multimodal-ai-assistant
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Install Python deps

```bash
pip install -r requirements.txt
# or minimal:
pip install streamlit ollama edge-tts pytesseract pillow pypdf2
```

### 3. Install System Deps

| OS          | Command                              |
| ----------- | ------------------------------------ |
| **Ubuntu**  | `sudo apt-get install tesseract-ocr` |
| **Windows** | `choco install tesseract`            |
| **macOS**   | `brew install tesseract`             |

### 4. Pull an LLM

```bash
ollama pull llama3:8b           # or tinyllama:1.1b, gemma:2b, etc.
```

### 5. Launch!

```bash
streamlit run main.py
```

> Your browser pops open at `http://localhost:8501`. Enjoy!

---

## ⚙️ Configuration

| Setting                 | How to change                                                               | Default           |
| ----------------------- | --------------------------------------------------------------------------- | ----------------- |
| **Model tag**           | `st.session_state["model_name"]` (sidebar) or hard-code in `ai_response.py` | `llama3`          |
| **Max response tokens** | `max_tokens` param in `ollama.chat()`                                       | `512`             |
| **Voice**               | Sidebar dropdown (Edge TTS voice short-names)                               | `en-US-GuyNeural` |
| **Reminder tone**       | Replace `assets/alert.mp3`                                                  | Soft ding         |
| **OCR language**        | `tesseract_cmd` + `lang='eng+hin'`                                          | `eng`             |

Environment variables (optional):

```bash
# .env.example
EDGE_TTS_PROXY=http://proxy:3128
STREAMLIT_SERVER_PORT=8502
```

---

## 📖 Usage Guide

<details>
<summary><strong>Chat</strong></summary>

1. Select **Chat** in sidebar.
2. Pick a model & temperature (slider).
3. Toggle **Speak replies** if you want TTS.
4. Type prompt → hit *Enter*.
5. Responses stream in; audio auto-plays if enabled.

</details>

<details>
<summary><strong>Diet Planner</strong></summary>

1. Switch to **Diet** tab.
2. Enter calories, dietary preference, allergies.
3. Click *Generate*.
4. Copy plan or have it read aloud.

</details>

<details>
<summary><strong>Reminders</strong></summary>

1. Go to **Reminders**.
2. Fill title + time (HH\:MM, 24-h).
3. Add → shows in list.
4. Keep the tab open; toast pops at set minute.

</details>

---

## 🛠 Extending the Assistant

| Add-on idea         | Where to start                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------ |
| **Image Chat**      | Wrap images in `ollama.chat(images=[bytes])` (needs multimodal model).                     |
| **Web Search Tool** | Create `modules/tools/web_search.py` with SerpAPI call and inject function-calling prompt. |
| **Persistent DB**   | Swap `st.session_state` for **SQLite** via SQLModel or Supabase.                           |
| **Docker**          | Write a lightweight `Dockerfile` installing Tesseract + Ollama (with GPU if CUDA).         |

---

## 🗂 Project Layout

```text
multimodal-ai-assistant/
├── main.py                # Streamlit UI & navigation
├── ai_response.py         # LLM chat / streaming logic
├── audio_output.py        # Edge-TTS wrapper
├── diet.py                # Diet plan generator
├── exercise.py            # Workout plan generator
├── reminders.py           # Client-side reminder logic
├── file_processing.py     # OCR + PDF parsing helpers
├── requirements.txt
├── assets/                # alert.mp3, screenshots, GIFs
└── README.md
```

---

## 🛑 Troubleshooting

| Symptom                         | Fix                                                              |
| ------------------------------- | ---------------------------------------------------------------- |
| **“TesseractNotFoundError”**    | Confirm `tesseract` on `$PATH`; run `tesseract --version`.       |
| **Edge-TTS fails behind proxy** | Set `EDGE_TTS_PROXY` env var.                                    |
| **LLM replies too slow**        | Use a smaller quantized model (`llama3:8b-q4_K_M`).              |
| **Reminders don’t fire**        | Keep tab focused OR disable browser “background tab throttling”. |

---

## 🗺 Roadmap

* [ ] **Persist reminders** to SQLite
* [ ] **RAG-powered document Q\&A** (embed uploaded PDFs, vector search)
* [ ] **Voice input** (Whisper CPP or Vosk)
* [ ] **Docker Compose** with Ollama GPU and Streamlit

---

## 🤝 Contributing

1. Fork → create feature branch → commit → PR.
2. Follow [Conventional Commits](https://www.conventionalcommits.org/).
3. Run `pre-commit install` to auto-format with **black** + **ruff**.

---

## 📜 License & Credits

*Code* released under the **MIT License**.
Built with ♥ using **Streamlit**, **Ollama**, **Edge-TTS**, and **Tesseract**.
Icons by [Phosphor](https://phosphoricons.com/).
Inspired by projects from @a16z-open-source and the Streamlit community.
