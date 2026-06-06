
# ⚖️ AI Cyber-Court

An interactive multi-agent AI simulation where LLMs battle it out in a futuristic courtroom. Submit a cybercrime scenario, watch a Prosecutor and Defense AI argue it out, vote as the Jury — then let the Judge AI decide if you got it right.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit) ![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎬 How It Works

1. **File a Case** — Type any cybercrime scenario. An AI validator checks it's actually arguable.
2. **The Debate** — A Prosecutor AI and Defense AI trade arguments across multiple turns, each rebutting the other.
3. **Jury Vote** — You vote Guilty or Not Guilty.
4. **The Verdict** — The Judge AI reads the full transcript, evaluates who argued better, and can **overrule your vote** if it thinks you're wrong. The verdict is read aloud via text-to-speech.
5. **Download** — Get a formatted PDF transcript of the entire trial.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.9+ |
| UI Framework | Streamlit |
| AI Model | Llama 3.3 70B via Groq API |
| PDF Generation | fpdf2 |
| Sound & Speech | Web Audio API + Web SpeechSynthesis (browser-native JS) |

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/ai-cyber-court.git
cd ai-cyber-court

# 2. Install dependencies
pip install streamlit openai fpdf2

# 3. Add your Groq API key to config.py
# Get a free key at: https://console.groq.com

# 4. Run
streamlit run main.py
```

> The app opens automatically at `http://localhost:8501`

---

## ⚙️ Configuration

In `config.py`:

```python
API_KEY  = "your_groq_api_key"   # Your Groq API key
MODEL    = "llama-3.3-70b-versatile"
MAX_TURNS = 4                     # Total arguments (2 prosecution + 2 defense)
```

---

## 📁 Project Structure

```
├── main.py            # Streamlit app & state machine
├── agents.py          # AI agent definitions & prompts
├── config.py          # API keys & settings
├── styles.py          # Custom CSS (dark futuristic theme)
├── sounds.py          # Browser sound synthesis & TTS
└── pdf_generator.py   # Court transcript PDF generation
```

---

## ✨ Cool Bits

- **Judge Overrule System** — The Judge AI can override your jury vote if it disagrees with your reasoning
- **No audio files** — All sounds are synthesized mathematically via the Web Audio API
- **Typewriter effect** — Built in pure Python, no JS required
- **AI Guardrails** — A validator agent rejects nonsense inputs before the trial starts

---

## 📄 License

MIT — free to use, modify, and share.
