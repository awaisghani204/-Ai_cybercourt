# ⚖️ The AI Cyber-Court: Project Documentation

Welcome to the **AI Cyber-Court**! This project is an interactive, multi-agent AI simulation where Large Language Models (LLMs) battle it out in a futuristic courtroom. 

This document explains exactly how the project works under the hood, the technology stack used, and the core concepts that bring the simulation to life.

---

## 🛠️ Technology Stack

- **Python**: The core programming language powering the backend logic.
- **Streamlit**: The web application framework. It handles the UI, layout, and state management without needing complex frontend frameworks like React.
- **OpenAI API**: The "brain" of the application. It generates the arguments for the Prosecutor, Defense, and the Judge.
- **fpdf2**: A Python library used to generate the downloadable Official Court Transcript as a formatted PDF.
- **Web Audio API (JavaScript)**: Used to generate synthetic, cinematic sound effects (like the gavel slam and voting beeps) directly in the browser.
- **Web SpeechSynthesis API (JavaScript)**: Used for the Text-to-Speech (TTS) engine that allows the Judge to speak the final verdict aloud.

---

## 🧠 Core Concepts

### 1. Multi-Agent LLM Roleplaying
Instead of a standard chatbot, this app uses multiple distinct "Agents." By carefully designing the **Prompts**, we force the AI to adopt specific personas:
- **The Prosecutor** is instructed to attack the defendant and point out guilt.
- **The Defense** is instructed to look at the Prosecutor's previous argument and find logical flaws.
- **The Judge** acts as an evaluator. It reads the entire transcript of the debate, evaluates who made the stronger logical arguments, and delivers a final verdict.

### 2. State Machine & Session State
Streamlit scripts usually run from top to bottom every time a user clicks a button. To create a multi-step game, we use a concept called a **State Machine**, tracked via `st.session_state.phase`:
- `Phase 0`: Case Input (Intake)
- `Phase 1`: The Debate (Turn-based arguments)
- `Phase 2`: Jury Vote (Human interaction)
- `Phase 3`: Final Verdict (Judge's ruling and PDF generation)

### 3. AI Guardrails (Input Validation)
LLMs are highly creative. If you tell them the crime is "2+2=4", they will invent a legal argument for why math is illegal! To prevent this, Phase 0 includes an **AI Intake Validator**. Before the trial starts, a hidden AI prompt evaluates the user's input. If it's a casual greeting or a math fact, the AI rejects it and dismisses the case.

### 4. Python-to-JavaScript Bridging
Streamlit is purely Python, which makes playing sounds difficult. We solved this by using `streamlit.components.v1`. When a sound needs to play, Python injects a tiny, invisible HTML `<iframe>` containing raw JavaScript into the browser. This JavaScript executes the Web Audio API and SpeechSynthesis API on the user's device.

---

## ⚙️ How the Application Works (Step-by-Step)

### Phase 0: Filing the Case
1. The user types a scenario (e.g., "Hacked the school database").
2. The **Validator Agent** (`agents.py`) secretly checks the input. If it's valid, the app moves to Phase 1.

### Phase 1: The Debate
1. The app alternates between the Prosecutor and the Defense for a set number of turns.
2. The Prosecutor looks at the crime and generates an opening statement.
3. The Defense takes the crime AND the Prosecutor's statement, and writes a rebuttal.
4. As the AI generates text, Streamlit renders it character-by-character using a loop and `time.sleep()`, creating a cool typewriter effect.

### Phase 2: The Jury Vote
1. The debate ends, and the human user (the Jury) is asked to vote **Guilty** or **Not Guilty**.
2. Clicking a button triggers a custom JavaScript sound effect and advances the phase.

### Phase 3: The Judge's Verdict & Overrule System
1. The app takes the entire debate history and the jury's vote, and sends it to the **Judge Agent**.
2. **The Overrule System**: The Judge evaluates the arguments objectively. If the human jury voted "Guilty" but the Defense clearly won the debate, the Judge will **overrule** the jury and explain why their decision was flawed!
3. The browser's Text-to-Speech engine reads the verdict aloud.
4. Finally, the app uses `fpdf2` to format the entire case history into an official PDF document, presenting a download button to the user.

---

## 🎨 Design & UI
The app avoids the "default Streamlit look" by injecting custom CSS (`styles.py`). It uses:
- **Glassmorphism**: Semi-transparent dark backgrounds with blur (`backdrop-filter`).
- **CSS Animations**: Chat bubbles sliding in from the sides, and pulsing buttons.
- **Chat App Layout**: Prosecution aligns to the left (Red/Pink), Defense to the right (Blue/Cyan), making it easy to read like a modern messaging app.
