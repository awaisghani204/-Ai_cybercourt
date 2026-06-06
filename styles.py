# Custom CSS and UI Styling definitions
import streamlit as st

def apply_custom_css():
    """Injects custom CSS into the Streamlit app."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');

        /* Dark futuristic theme & edge-to-edge layout */
        .stApp {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a1628 100%);
        }
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: rgba(10, 10, 25, 0.6) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(123, 47, 255, 0.3);
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }

        /* Main title */
        .court-title {
            text-align: center;
            padding: 10px 0 10px 0;
        }
        .court-title h1 {
            font-family: 'Orbitron', monospace;
            font-size: 2.8rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00f0ff, #7b2fff, #ff2d95);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: none;
            animation: glow 3s ease-in-out infinite alternate;
            margin-bottom: 0;
        }
        .court-subtitle {
            text-align: center;
            font-family: 'Inter', sans-serif;
            color: #8892b0;
            font-size: 1rem;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        @keyframes glow {
            from { filter: drop-shadow(0 0 10px rgba(0, 240, 255, 0.3)); }
            to { filter: drop-shadow(0 0 25px rgba(123, 47, 255, 0.5)); }
        }

        /* Divider */
        .neon-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #00f0ff, #7b2fff, #ff2d95, transparent);
            border: none;
            margin: 15px 0 25px 0;
            border-radius: 2px;
        }

        /* Input Fields Styling */
        div[data-baseweb="input"] > div {
            background-color: rgba(15, 15, 40, 0.8) !important;
            border: 1px solid rgba(123, 47, 255, 0.4) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }
        div[data-baseweb="input"] > div:focus-within {
            border-color: #00f0ff !important;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.3) !important;
        }
        input {
            color: #e0e0f0 !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Chat Bubbles Layout */
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .chat-prosecutor {
            align-self: flex-start;
            max-width: 85%;
            background: linear-gradient(145deg, rgba(255, 30, 30, 0.1), rgba(15, 15, 40, 0.95));
            border: 1px solid rgba(255, 45, 149, 0.4);
            border-left: 4px solid #ff2d95;
            border-radius: 12px 12px 12px 0;
            padding: 20px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
            animation: fadeSlideRight 0.4s ease-out;
        }
        
        .chat-defense {
            align-self: flex-end;
            max-width: 85%;
            background: linear-gradient(145deg, rgba(0, 200, 255, 0.1), rgba(15, 15, 40, 0.95));
            border: 1px solid rgba(0, 240, 255, 0.4);
            border-right: 4px solid #00f0ff;
            border-radius: 12px 12px 0 12px;
            padding: 20px;
            text-align: right;
            box-shadow: -5px 5px 15px rgba(0,0,0,0.3);
            animation: fadeSlideLeft 0.4s ease-out;
        }

        .chat-prosecutor h3, .chat-defense h3 {
            font-family: 'Orbitron', monospace;
            font-size: 0.9rem;
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        .chat-prosecutor h3 { color: #ff2d95; }
        .chat-defense h3 { color: #00f0ff; }

        .chat-prosecutor p, .chat-defense p {
            color: #c8ccd8;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            font-size: 1rem;
            margin: 0;
        }

        @keyframes fadeSlideRight {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes fadeSlideLeft {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        /* Verdict card */
        .verdict-card {
            background: linear-gradient(145deg, rgba(123, 47, 255, 0.15), rgba(15, 15, 40, 0.95));
            border: 2px solid rgba(123, 47, 255, 0.6);
            border-radius: 20px;
            padding: 30px;
            margin: 30px auto;
            max-width: 90%;
            text-align: center;
            animation: verdictReveal 1.2s ease-out;
            box-shadow: 0 0 40px rgba(123, 47, 255, 0.2);
            backdrop-filter: blur(15px);
        }
        .verdict-card h2 {
            font-family: 'Orbitron', monospace;
            color: #7b2fff;
            font-size: 1.5rem;
            margin-bottom: 20px;
        }
        .verdict-card p {
            color: #e0e0f0;
            font-family: 'Inter', sans-serif;
            line-height: 1.9;
            font-size: 1.05rem;
            text-align: left;
        }

        @keyframes verdictReveal {
            0% { opacity: 0; transform: scale(0.9); border-color: transparent; }
            50% { border-color: rgba(255, 45, 149, 0.8); box-shadow: 0 0 60px rgba(255, 45, 149, 0.4); }
            100% { opacity: 1; transform: scale(1); border-color: rgba(123, 47, 255, 0.6); }
        }

        /* Phase header */
        .phase-header {
            font-family: 'Orbitron', monospace;
            font-size: 1.2rem;
            font-weight: 700;
            text-align: center;
            padding: 10px;
            margin: 15px 0;
            color: #ffffff;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        /* Jury section */
        .jury-section {
            text-align: center;
            padding: 25px;
            background: rgba(15, 15, 40, 0.7);
            border: 1px solid rgba(123, 47, 255, 0.3);
            border-radius: 16px;
            margin: 20px auto;
            max-width: 80%;
            backdrop-filter: blur(10px);
        }
        .jury-section h3 {
            font-family: 'Orbitron', monospace;
            color: #ffd700;
            font-size: 1.2rem;
        }
        .jury-section p {
            color: #8892b0;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
        }

        /* Vote result badge */
        .vote-badge {
            display: inline-block;
            padding: 10px 30px;
            border-radius: 30px;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 2px;
            animation: pulseBadge 2s ease-in-out infinite;
            margin-bottom: 10px;
        }
        .vote-guilty {
            background: linear-gradient(135deg, #ff2d55, #ff6b6b);
            color: #fff;
            box-shadow: 0 0 20px rgba(255, 45, 85, 0.5);
        }
        .vote-not-guilty {
            background: linear-gradient(135deg, #00c853, #69f0ae);
            color: #0a0a1a;
            box-shadow: 0 0 20px rgba(0, 200, 83, 0.5);
        }

        @keyframes pulseBadge {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        /* Sidebar Progress Tracker Customization */
        .sidebar-title {
            font-family: 'Orbitron', monospace;
            color: #ffffff;
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.2rem;
            letter-spacing: 2px;
        }
        .sidebar-case {
            background: rgba(123, 47, 255, 0.1);
            border: 1px solid rgba(123, 47, 255, 0.4);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 30px;
        }
        .sidebar-case h4 {
            font-family: 'Orbitron', monospace;
            color: #00f0ff;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }
        .sidebar-case p {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #e0e0f0;
            margin: 0;
        }

        .progress-step-sidebar {
            padding: 12px 15px;
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
        }
        .step-done {
            background: rgba(0, 240, 255, 0.1);
            color: #00f0ff;
            border-left: 4px solid #00f0ff;
        }
        .step-active {
            background: rgba(123, 47, 255, 0.2);
            color: #c4a0ff;
            border-left: 4px solid #7b2fff;
            animation: subtlePulse 2s infinite;
        }
        .step-pending {
            background: rgba(255, 255, 255, 0.03);
            color: #5a5a7a;
            border-left: 4px solid #3a3a5a;
        }

        @keyframes subtlePulse {
            0%, 100% { box-shadow: inset 0 0 0px transparent; }
            50% { box-shadow: inset 200px 0 30px rgba(123, 47, 255, 0.1); }
        }

        /* Button styling */
        .stButton > button {
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            padding: 12px 30px !important;
            font-size: 1.05rem !important;
            transition: all 0.3s ease !important;
            letter-spacing: 1px !important;
            border: 1px solid rgba(123, 47, 255, 0.6) !important;
            background: rgba(20, 20, 50, 0.8) !important;
            color: #ffffff !important;
        }
        .stButton > button:hover {
            transform: scale(1.03) translateY(-2px) !important;
            box-shadow: 0 10px 20px rgba(123, 47, 255, 0.3) !important;
            border-color: #00f0ff !important;
            color: #00f0ff !important;
        }

        /* Typing cursor animation */
        .typing-cursor {
            display: inline;
            color: #00f0ff;
            font-weight: 700;
            animation: blink-cursor 0.6s step-end infinite;
        }

        @keyframes blink-cursor {
            from, to { opacity: 1; }
            50% { opacity: 0; }
        }

        /* Hide default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        iframe[height="0"] { position: absolute; visibility: hidden; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)
