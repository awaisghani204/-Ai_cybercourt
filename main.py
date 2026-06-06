import asyncio
import sys

# Fix for Python 3.14+ compatibility with Streamlit
# Python 3.14 removed implicit event loop creation in asyncio.get_event_loop()
if sys.version_info >= (3, 14):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

import streamlit as st
import time

# Import configurations and agents from our new modules
from config import MAX_TURNS
from styles import apply_custom_css
from sounds import play_sound, speak_verdict
from agents import (
    generate_prosecutor_statement, 
    generate_defense_statement, 
    generate_judge_verdict
)

# ==========================================
# 1. PAGE CONFIG & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="AI Cyber-Court", page_icon="⚖️", layout="wide")
apply_custom_css()

# ==========================================
# 2. SESSION STATE
# ==========================================
if "phase" not in st.session_state:
    st.session_state.phase = 0  # 0=input, 1=debate, 2=jury, 3=verdict
if "debate_history" not in st.session_state:
    st.session_state.debate_history = []  # List of {"role": "Prosecutor" / "Defense", "text": "..."}
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "jury_vote" not in st.session_state:
    st.session_state.jury_vote = None
if "final_verdict" not in st.session_state:
    st.session_state.final_verdict = ""
if "crime" not in st.session_state:
    st.session_state.crime = ""
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

# ==========================================
# 3. HEADER
# ==========================================
st.markdown("""
<div class="court-title">
    <h1>⚖️ THE AI CYBER-COURT ⚖️</h1>
</div>
<div class="court-subtitle">Interactive Legal Simulation • Powered by AI</div>
<div class="neon-divider"></div>
""", unsafe_allow_html=True)

# ==========================================
# 4. PROGRESS TRACKER
# ==========================================
phase = st.session_state.phase
labels = ["📝 CASE FILED", "🗣️ THE DEBATE", "🗳️ JURY VOTE", "📜 VERDICT"]

with st.sidebar:
    st.markdown('<div class="sidebar-title">COURT STATUS</div>', unsafe_allow_html=True)
    
    if st.session_state.crime:
        st.markdown(f"""
        <div class="sidebar-case">
            <h4>CURRENT CASE</h4>
            <p>{st.session_state.crime}</p>
        </div>
        """, unsafe_allow_html=True)
        
    for i, label in enumerate(labels):
        if i < phase:
            cls = "step-done"
            icon = "✓"
        elif i == phase:
            cls = "step-active"
            icon = "▶"
        else:
            cls = "step-pending"
            icon = "○"
        st.markdown(f'<div class="progress-step-sidebar {cls}"><span>{icon}</span> {label}</div>', unsafe_allow_html=True)

# ==========================================
# 5. PHASE 0: CASE INPUT
# ==========================================
if phase == 0:
    st.markdown('<div class="phase-header"><span class="phase-number">1</span> FILE YOUR CASE</div>', unsafe_allow_html=True)
    
    crime_description = st.text_input(
        "Enter the Cybercrime for today's trial:",
        placeholder="e.g., Hacking the university portal to change grades",
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div style="text-align: center; color: #8892b0; font-family: 'Inter', sans-serif; font-size: 0.85rem; margin: -10px 0 15px 0;">
        💡 <em>Describe a cybercrime scenario — the AI attorneys will battle it out!</em>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        if st.button("⚖️ COMMENCE TRIAL", use_container_width=True, type="primary"):
            if crime_description:
                with st.spinner("Analyzing case validity..."):
                    from agents import validate_case
                    is_valid, reason = validate_case(crime_description)
                if is_valid:
                    st.session_state.crime = crime_description
                    st.session_state.phase = 1
                    st.session_state.debate_history = []
                    st.session_state.turn = 0
                    play_sound("gavel")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error(f"Case Dismissed: {reason}")
            else:
                st.warning("⚠️ Please describe a cybercrime first!")

# ==========================================
# 6. PHASE 1: THE DEBATE
# ==========================================
elif phase == 1:
    st.markdown('<div class="phase-header"><span class="phase-number">2</span> THE DEBATE</div>', unsafe_allow_html=True)
    
    # Render all previous arguments
    for msg in st.session_state.debate_history:
        if msg["role"] == "Prosecutor":
            st.markdown(f"""
            <div class="chat-container">
                <div class="chat-prosecutor">
                    <h3>🏛️ PROSECUTION</h3>
                    <p>{msg["text"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-container">
                <div class="chat-defense">
                    <h3>🛡️ DEFENSE</h3>
                    <p>{msg["text"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)

    # Next Turn Logic
    if st.session_state.turn < MAX_TURNS:
        is_prosecutor_turn = (st.session_state.turn % 2 == 0)
        btn_label = "🏛️ PROSECUTOR SPEAKS" if is_prosecutor_turn else "🛡️ DEFENSE RESPONDS"
        spinner_msg = "The Cyber-Prosecutor is preparing..." if is_prosecutor_turn else "The Defense Attorney is crafting a rebuttal..."
        
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button(btn_label, use_container_width=True, type="primary"):
                with st.spinner(spinner_msg):
                    try:
                        if is_prosecutor_turn:
                            previous = st.session_state.debate_history[-1]['text'] if st.session_state.turn > 0 else None
                            response_text = generate_prosecutor_statement(st.session_state.crime, previous)
                        else:
                            previous = st.session_state.debate_history[-1]['text']
                            response_text = generate_defense_statement(st.session_state.crime, previous)
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.stop()

                # Sound effect
                play_sound("notification")

                # Typewriter animation
                role_class = "chat-prosecutor" if is_prosecutor_turn else "chat-defense"
                role_title = "🏛️ PROSECUTION" if is_prosecutor_turn else "🛡️ DEFENSE"
                placeholder = st.empty()
                typed = ""
                for i, char in enumerate(response_text):
                    typed += char
                    if i % 3 == 0 or i == len(response_text) - 1:
                        placeholder.markdown(f"""
                        <div class="chat-container">
                            <div class="{role_class}">
                                <h3>{role_title}</h3>
                                <p>{typed}<span class="typing-cursor">▌</span></p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.01)

                # Final render without cursor
                placeholder.markdown(f"""
                <div class="chat-container">
                    <div class="{role_class}">
                        <h3>{role_title}</h3>
                        <p>{response_text}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Save to history and continue
                st.session_state.debate_history.append({
                    "role": "Prosecutor" if is_prosecutor_turn else "Defense",
                    "text": response_text
                })
                st.session_state.turn += 1
                time.sleep(0.3)
                st.rerun()
                        
    else:
        # End of debate, move to jury vote
        st.info("The debate has concluded. The fate of the defendant is now in the hands of the jury.")
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button("🗳️ PROCEED TO JURY VOTE →", use_container_width=True, type="primary"):
                st.session_state.phase = 2
                st.rerun()

# ==========================================
# 7. PHASE 2: JURY VOTE
# ==========================================
elif phase == 2:
    st.markdown('<div class="phase-header"><span class="phase-number">3</span> JURY VOTE</div>', unsafe_allow_html=True)
    
    with st.expander("📂 Review Full Debate", expanded=False):
        for msg in st.session_state.debate_history:
            role_icon = "🏛️" if msg["role"] == "Prosecutor" else "🛡️"
            css_class = "chat-prosecutor" if msg["role"] == "Prosecutor" else "chat-defense"
            st.markdown(f"""
            <div class="chat-container">
                <div class="{css_class}" style="padding: 15px; margin: 10px 0;">
                    <h3 style="font-size: 0.9rem; margin-bottom: 5px;">{role_icon} {msg["role"].upper()}</h3>
                    <p style="font-size: 0.9rem;">{msg["text"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("""
    <div class="jury-section">
        <h3>🗳️ THE JURY MUST DECIDE</h3>
        <p>You have heard the arguments back and forth. It's time to deliver your verdict.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 GUILTY", use_container_width=True):
            st.session_state.jury_vote = "Guilty"
            st.session_state.phase = 3
            play_sound("vote")
            time.sleep(0.3)
            st.rerun()
    with col2:
        if st.button("✅ NOT GUILTY", use_container_width=True):
            st.session_state.jury_vote = "Not Guilty"
            st.session_state.phase = 3
            play_sound("vote")
            time.sleep(0.3)
            st.rerun()

# ==========================================
# 8. PHASE 3: FINAL VERDICT
# ==========================================
elif phase == 3:
    # Show jury vote badge
    vote = st.session_state.jury_vote
    badge_class = "vote-guilty" if vote == "Guilty" else "vote-not-guilty"
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <span class="vote-badge {badge_class}">JURY VOTED: {vote.upper()}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="phase-header"><span class="phase-number">4</span> THE JUDGE SPEAKS</div>', unsafe_allow_html=True)
    
    if not st.session_state.final_verdict:
        with st.spinner("📜 The Supreme Cyber-Judge is deliberating..."):
            try:
                verdict_text = generate_judge_verdict(
                    st.session_state.crime, 
                    st.session_state.debate_history, 
                    st.session_state.jury_vote
                )
                
                # Compile history for transcript saving (PDF)
                from pdf_generator import generate_transcript_pdf
                pdf_bytes = generate_transcript_pdf(
                    st.session_state.crime,
                    st.session_state.debate_history,
                    st.session_state.jury_vote,
                    verdict_text
                )
                st.session_state.pdf_bytes = pdf_bytes
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        # Dramatic verdict sound + gavel
        play_sound("verdict")
        time.sleep(0.3)
        play_sound("gavel")

        # Typewriter effect for the verdict
        placeholder = st.empty()
        typed = ""
        for i, char in enumerate(verdict_text):
            typed += char
            if i % 3 == 0 or i == len(verdict_text) - 1:
                placeholder.markdown(f"""
                <div class="verdict-card">
                    <h2>📜 FINAL VERDICT</h2>
                    <p>{typed}<span class="typing-cursor">▌</span></p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.01)

        # Final render without cursor
        placeholder.markdown(f"""
        <div class="verdict-card">
            <h2>📜 FINAL VERDICT</h2>
            <p>{verdict_text}</p>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.final_verdict = verdict_text
        st.balloons()

        # Judge speaks the verdict aloud
        speak_verdict(verdict_text)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.pdf_bytes:
            st.download_button(
                label="📄 Download Official Court Transcript (PDF)",
                data=st.session_state.pdf_bytes,
                file_name="official_transcript.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
                key="dl_btn_1"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button("🔄 START NEW TRIAL", use_container_width=True, type="secondary", key="restart_1"):
                st.session_state.phase = 0
                st.session_state.debate_history = []
                st.session_state.turn = 0
                st.session_state.jury_vote = None
                st.session_state.final_verdict = ""
                st.session_state.crime = ""
                st.session_state.pdf_bytes = None
                st.rerun()
    
    elif st.session_state.final_verdict:
        st.markdown(f"""
        <div class="verdict-card">
            <h2>📜 FINAL VERDICT</h2>
            <p>{st.session_state.final_verdict}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.pdf_bytes:
            st.download_button(
                label="📄 Download Official Court Transcript (PDF)",
                data=st.session_state.pdf_bytes,
                file_name="official_transcript.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
                key="dl_btn_2"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button("🔄 START NEW TRIAL", use_container_width=True, type="secondary", key="restart_2"):
                st.session_state.phase = 0
                st.session_state.debate_history = []
                st.session_state.turn = 0
                st.session_state.jury_vote = None
                st.session_state.final_verdict = ""
                st.session_state.crime = ""
                st.session_state.pdf_bytes = None
                st.rerun()