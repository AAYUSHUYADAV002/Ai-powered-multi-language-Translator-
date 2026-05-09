import streamlit as st
import os
from dotenv import load_dotenv
import sys
from pathlib import Path
import tempfile
import time

sys.path.append(str(Path(__file__).resolve().parent.parent))

from translator import Translator, TranslatorConfig



# 1. Load your .env file

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
# 2. Page Configuration
st.set_page_config(
    page_title="NEXUS | Universal Translator",
    page_icon="🌐",
    layout="wide"
)

# --- TOP NAVIGATION BAR CSS ---
st.markdown("""
    <style>
    /* Fixed Top Nav Bar */
    .top-nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(34, 211, 238, 0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        z-index: 999999;
    }
    
    .nav-logo {
        font-weight: 900;
        font-size: 22px;
        background: linear-gradient(to right, #22d3ee, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nav-user {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 500;
    }

    /* Padding to prevent content from going under the Nav Bar */
    .stMainBlockContainer {
        padding-top: 80px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INJECT THE NAV BAR ---
# We check if the user is logged in to show their name
user_display = st.session_state.user if st.session_state.get("logged_in") else "Guest"

st.markdown(f"""
    <div class="top-nav">
        <div class="nav-logo">⚡ NEXUS AI</div>
        <div class="nav-user">🟢 Online: {user_display}</div>
    </div>
    """, unsafe_allow_html=True)

# --- THEME CSS (Matches app.py) ---
st.markdown("""
    <style>
    .stApp { background: #020617; }
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(34, 211, 238, 0.2);
    }
    /* --- HIDE DEFAULT SIDEBAR NAVIGATION --- */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Optional: If 'app' is still showing, this targets the very top list */
    [data-testid="stSidebarNav"] ul {
        display: none !important;
    }
    /* Top Nav Bar Emulation */
    .top-nav-emu {
        background: rgba(15, 23, 42, 0.8);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(34, 211, 238, 0.3);
        margin-bottom: 25px;
    }

    /* Input Field Visibility */
    textarea, input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }

    /* Glassmorphism for Result Boxes */
    .result-box {
        background: rgba(30, 41, 59, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #22d3ee;
        color: #f8fafc;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #06b6d4, #8b5cf6) !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
    }
    
    /* 1. Language Selectbox Styling */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #22d3ee !important;
        border-radius: 10px !important;
    }

    /* 2. Drag & Drop File Uploader Styling */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 2px dashed #22d3ee !important;
        border-radius: 15px !important;
        padding: 20px !important;
        transition: 0.3s;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(34, 211, 238, 0.05) !important;
        border-color: #8b5cf6 !important; /* Changes to Purple on hover */
    }

    /* 3. Fixing the 'Browse Files' button inside Uploader */
    [data-testid="stFileUploader"] button {
        background: #06b6d4 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
    }

    /* 4. Selectbox Text Color */
    div[data-testid="stSelectbox"] label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        margin-bottom: 8px;
    }
    
    
    /* --- MULTIMEDIA BLOCK VIBE --- */
    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.6) !important; /* Dark Slate Glass */
        border: 2px dashed #22d3ee !important; /* Neon Cyan Dashed Border */
        border-radius: 20px !important;
        padding: 40px !important;
        transition: all 0.4s ease-in-out !important;
        box-shadow: inset 0 0 20px rgba(34, 211, 238, 0.05) !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #a855f7 !important; /* Switch to Purple on Hover */
        background: rgba(34, 211, 238, 0.05) !important;
        box-shadow: 0 0 30px rgba(34, 211, 238, 0.15) !important;
    }

    /* Target the 'Browse Files' button inside the uploader */
    [data-testid="stFileUploaderDropzone"] button {
        background: linear-gradient(90deg, #06b6d4, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        padding: 10px 25px !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Change the color of the 'Drag and drop' text */
    [data-testid="stFileUploader"] section > div > div > span {
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }
    
    /* Change the color of the cloud/upload icon */
    [data-testid="stFileUploader"] svg {
        fill: #22d3ee !important;
    }
    /* Back Button Specifics */
    .back-btn > div > button {
        background: transparent !important;
        border: 1px solid #334155 !important;
        color: #94a3b8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.markdown("### ⬅️ Navigation")
    if st.button("BACK TO DASHBOARD", use_container_width=True):
        st.switch_page("app.py")
    
    st.divider()
    st.header("⚙️ Settings")
    src_lang = st.selectbox("Source Language", ["English", "Hindi", "Spanish","Arabic","Korean","Tamil","Marathi","Sanskrit","Gujarati","Punjabi","Japanese","Russian","Bengali","Mandarin Chinese", "French"])
    tgt_lang = st.selectbox("Target Language", ["Hindi", "English", "Spanish","Arabic","Korean","Tamil","Marathi","Sanskrit","Gujarati","Punjabi","Japanese","Russian","Bengali","Mandarin Chinese", "French"], index=1)

# 4. Initialize Translator Engine
@st.cache_resource

def get_translator_engine(source, target):

    if not api_key:

        st.error("❌ API Key not found! Please check your .env file.")

        return None

       

    try:

        cfg = TranslatorConfig(

            source_language=source,

            target_language=target,

            model="gemini-2.5-flash",

            model_provider="google_genai"

        )

        return Translator(config=cfg)

    except Exception as e:

        st.error(f"⚠️ Initialization Error: {e}")

        return None



# Create translator instance

translator = get_translator_engine(src_lang, tgt_lang)
# --- MAIN INTERFACE ---
st.markdown("<div class='top-nav-emu'><h2 style='margin:0; text-align:center; color:#22d3ee !important;'>⚡ UNIVERSAL TRANSLATOR</h2></div>", unsafe_allow_html=True)


# Text Area Section
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📥 Source Text")
    st.markdown("""
    <style>
    textarea {
        color: white !important;
        -webkit-text-fill-color: white !important;
        background-color: #1e293b !important;
    }
    </style>
    """, unsafe_allow_html=True)
    user_text = st.text_area("", placeholder="Type your text here...", height=250, label_visibility="collapsed")
    
    if st.button("TRANSLATE TEXT ✨", use_container_width=True):
        if not user_text:
            st.warning("Please enter text.")
        elif translator:
            with st.spinner("AI Processing..."):
                try:
                    # Update translator with new languages before translating
                    translator.config.source_language = src_lang
                    translator.config.target_language = tgt_lang
                    result = translator.translate(user_text)
                    st.session_state.last_result = result
                except Exception as e:
                    st.error(f"Error: {e}")

with col2:
    st.markdown("### 📤 AI Result")
    if "last_result" in st.session_state:
        st.markdown("""
        <style>
        textarea {
            color: white !important;
            -webkit-text-fill-color: white !important;
            background-color: #1e293b !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="result-box" style="height:250px; overflow-y:auto;">{st.session_state.last_result}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
    <style>
    textarea {
        color: white !important;
        -webkit-text-fill-color: white !important;
        background-color: #1e293b !important;
    }
    </style>
    """, unsafe_allow_html=True)
        st.markdown('<div class="result-box" style="height:250px; border-style: dashed; border-color: #334155; display:flex; align-items:center; justify-content:center; color:#64748b !important;">Translation will appear here...</div>', unsafe_allow_html=True)

st.divider()

# --- MEDIA SECTION ---
st.markdown("""
    <div style='background: rgba(34, 211, 238, 0.1); padding: 10px; border-radius: 10px; border-left: 5px solid #22d3ee; margin-bottom: 20px;'>
        <h3 style='margin:0; color: #f8fafc !important;'>📁 Multimedia Intelligence</h3>
        <p style='margin:0; color: #94a3b8 !important; font-size: 14px;'>Upload MP3 or MP4 for AI-powered Transcription & Translation</p>
    </div>
    """, unsafe_allow_html=True)

# The themed uploader
uploaded_file = st.file_uploader("", type=["mp3", "mp4"], label_visibility="collapsed")

if uploaded_file:
    # Small status indicator for the file
    st.markdown(f"📦 **File Detected:** `{uploaded_file.name}`")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        temp_file_path = tmp.name

    # Bright Action Button
    if st.button("🚀 EXECUTE MULTIMEDIA TRANSLATION", use_container_width=True):
        with st.spinner("AI is analyzing media..."):
            try:
                # Assuming translator.py has this method
                result = translator.translate_media(temp_file_path)
                st.markdown("#### 📝 Analysis Result:")
                st.markdown(f'<div class="result-box" style="border-color: #a855f7;">{result}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Analysis Error: {e}")
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid #334155; padding-top: 20px;'>
        <p style='color: #475569 !important; font-size: 12px;'>
            SYSTEM: NEXUS CORE  | OPERATOR: {st.session_state.user} 
        </p>
    </div>
    """, unsafe_allow_html=True)