import streamlit as st
import google.generativeai as genai
from docx import Document
from pypdf import PdfReader
import io
import os
import time
from dotenv import load_dotenv

# --- 1. CONFIG & API SETUP ---
st.set_page_config(page_title="NEXUS | Enterprise", page_icon="🏢", layout="wide")
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        API_READY = True
    except Exception as e:
        API_READY = False
        API_ERR = str(e)
else:
    API_READY = False
    API_ERR = "API Key not found in .env"

# --- 2. THE ULTIMATE THEME OVERRIDE (FIXES ALL WHITE PARTS) ---
st.markdown("""
    <style>
    /* 1. Global Background and Text */
    .stApp { background-color: #020617 !important; }
    * { color: #f8fafc !important; font-family: 'Inter', sans-serif; }

    /* 2. Fix the File Uploader (Brute Force) */
    [data-testid="stFileUploadDropzone"] {
        background-color: #0f172a !important;
        border: 2px dashed #22d3ee !important;
        border-radius: 12px !important;
        color: #22d3ee !important;
    }
    /* Fix 'Browse files' button text color */
    [data-testid="stFileUploadDropzone"] button {
        background-color: #1e293b !important;
        color: #22d3ee !important;
        border: 1px solid #22d3ee !important;
    }
    /* Fix small text like "Limit 200MB per file" */
    [data-testid="stFileUploadDropzone"] small { color: #94a3b8 !important; }

    /* 3. Fix the Selectbox/Dropdown (White Box Fix) */
    div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        border: 1px solid #22d3ee !important;
    }
    /* Fix dropdown chevron icon */
    div[data-baseweb="select"] svg { fill: #22d3ee !important; }

    /* 4. Fix Radio Buttons */
    [data-testid="stWidgetLabel"] p { color: #c084fc !important; font-weight: bold !important; }
    div[data-testid="stMarkdownContainer"] p { color: #f8fafc !important; }

    /* 5. Buttons - Initiate (Cyan) vs Download (Purple) */
    .stButton > button {
        background: linear-gradient(90deg, #06b6d4, #3b82f6) !important;
        color: white !important; width: 100%; border: none !important;
        font-weight: 800 !important; text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.2) !important;
    }
    
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(90deg, #8b5cf6, #d946ef) !important;
        color: white !important; border: none !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }
     
    [data-testid="stSidebarNav"] {
    display: none !important;
}

    /* 6. Navigation Bar & Sidebar */
    .top-nav {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(34, 211, 238, 0.3);
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 40px; z-index: 999999;
    }
    .nav-logo { font-weight: 900; font-size: 22px; background: linear-gradient(to right, #22d3ee, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stMainBlockContainer { padding-top: 100px !important; }
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #22d3ee !important; }

    /* 7. Result Box */
    .doc-card {
        background: rgba(30, 41, 59, 0.4); padding: 25px;
        border-radius: 15px; border: 1px solid #8b5cf6;
        min-height: 400px; line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# UI Elements
st.markdown(f'<div class="top-nav"><div class="nav-logo">⚡ NEXUS AI</div><div style="color: #94a3b8;">🏢 Enterprise Module</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⬅️ Navigation")
    if st.button("BACK TO DASHBOARD", use_container_width=True):
        st.switch_page("app.py")

# --- 3. HELPER LOGIC ---
def extract_text(file):
    if file.name.lower().endswith('.docx'):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file.name.lower().endswith('.pdf'):
        reader = PdfReader(file)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    return file.read().decode("utf-8")

# --- 4. INTERFACE ---
st.markdown("<h2 style='text-align:center; color:#22d3ee !important;'>🏢 Enterprise Intelligence Hub</h2>", unsafe_allow_html=True)

if not API_READY:
    st.error(f"Engine Failure: {API_ERR}")
else:
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown("### 📥 Document Intake")
        st.markdown("""
            <style>
                /* 1. Box Background and Border */
                .stFileUploader {
                    background-color: #0f172a !important;
                    padding: 20px !important;
                    border-radius: 15px !important;
                    border: 1px solid rgba(34, 211, 238, 0.4) !important;
                }

                /* 2. TARGET: The Upload Icon (SVG) - Making it Blue */
                .stFileUploader svg {
                    fill: #22d3ee !important;
                    color: #22d3ee !important;
                }

                /* 3. Drag and Drop Main Text (Cyan) */
                .stFileUploader section div div span {
                    color: #1e293b !important;
                }

                /* 4. Limit 200MB text (Dark Gray) */
                .stFileUploader section div div small {
                    color: #475569 !important;
                }

                /* 5. Browse Files Button */
                .stFileUploader button {
                    background-color: #1e293b !important;
                    color: white !important;
                    border: 1px solid #22d3ee !important;
                    border-radius: 8px !important;
                }
            </style>
               """, unsafe_allow_html=True)
        file = st.file_uploader("Upload corporate file (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])
        target_lang = st.selectbox("Intelligence Target", ["English", "Hindi", "Spanish", "German", "Japanese"])
        action = st.radio("Intelligence Protocol", ["Executive Summary", "Full Translation", "Action Item Extraction"])

        if st.button("INITIATE NEURAL SCAN"):
            if file:
                with st.spinner("AI Analysis in Progress..."):
                    try:
                        raw_content = extract_text(file)
                        prompt = f"As a professional AI analyst, provide a {action} of this text in {target_lang}: \n\n{raw_content[:8000]}"
                        response = model.generate_content(prompt)
                        st.session_state.ent_report = response.text
                    except Exception as e:
                        st.error(f"Fault: {e}")
            else:
                st.warning("No document detected.")

    with col2:
        st.markdown("### 📤 Intelligence Output")
        report = st.session_state.get("ent_report", "Awaiting document uplink...")
        st.markdown(f'<div class="doc-card">{report}</div>', unsafe_allow_html=True)
        
        if "ent_report" in st.session_state:
            st.write("")
            st.download_button("💾 DOWNLOAD ANALYSIS REPORT", data=st.session_state.ent_report, file_name="NEXUS_Report.txt")

st.markdown("<br><hr><center><p style='color: #475569 !important; font-size: 11px;'>NEXUS SECURE PIPELINE | SVVV 2026 | OPERATOR: Ayushi</p></center>", unsafe_allow_html=True)