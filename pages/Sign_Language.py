import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request
import time

# --- 1. AUTO-DOWNLOAD AI BRAIN ---
MODEL_PATH = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

def ensure_model_exists():
    if not os.path.exists(MODEL_PATH):
        try:
            with st.spinner("Initializing AI Core... Downloading Model."):
                urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        except Exception as e:
            st.error(f"Download Error: {e}")

# --- 2. PAGE CONFIG & NEXUS THEME ---
st.set_page_config(page_title="NEXUS | Sign Bridge", page_icon="🤟", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = "Guest"

st.markdown("""
    <style>
    .stApp { background: #020617; }
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    
    .top-nav {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(34, 211, 238, 0.3);
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 40px; z-index: 999999;
    }
    .nav-logo {
        font-weight: 900; font-size: 22px;
        background: linear-gradient(to right, #22d3ee, #c084fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .stMainBlockContainer { padding-top: 80px !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(34, 211, 238, 0.2);
    }
    
    .result-box {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px; border-radius: 15px; border: 1px solid #8b5cf6;
        color: #ffffff !important; text-align: center;
        font-size: 28px; font-weight: bold;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
    }
            
    /* NEXUS Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #06b6d4, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
        background: linear-gradient(90deg, #22d3ee, #a78bfa) !important;
    }

    /* Sidebar Background Fix */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(34, 211, 238, 0.2);
    }
            
    .stImage > img {
        border: 2px solid #22d3ee; border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation Bar
st.markdown(f'<div class="top-nav"><div class="nav-logo">⚡ NEXUS AI</div><div style="color: #94a3b8;">🟢 {st.session_state.user} | Sign Bridge Active</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⬅️ Navigation")
    if st.button("BACK TO DASHBOARD", use_container_width=True):
        st.switch_page("app.py")
    st.divider()
    st.info("Module: Hand Gesture Neural Analysis (Vision Task API)")

# --- 3. VISION ENGINE INITIALIZATION ---
ensure_model_exists()

@st.cache_resource
def load_vision_detector():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1
    )
    return vision.HandLandmarker.create_from_options(options)

detector = load_vision_detector()

# --- 4. MAIN INTERFACE ---
st.markdown("<h2 style='text-align:center; color:#22d3ee !important;'>🤟 Sign Bridge: Real-Time Neural Feed</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### 📝 AI Output")
    # THE FIX: Empty placeholder for live updates
    output_placeholder = st.empty()
    output_placeholder.markdown(f'<div class="result-box"><small style="color:#94a3b8">AI PREDICTION</small><br>Offline</div>', unsafe_allow_html=True)
    
    st.write("")
 

with col1:
    st.markdown("### 📷 Neural Vision Feed")
    run = st.toggle("ACTIVATE CAMERA SCANNER", value=False)
    FRAME_WINDOW = st.image([])
    
    if run:
        cap = cv2.VideoCapture(0)
        while run:
            success, frame = cap.read()
            if not success: break
            
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # Use real-time timestamp
            ms_timestamp = int(time.time() * 1000)
            result = detector.detect_for_video(mp_image, ms_timestamp)
            
            label = "Scanning..."
            
            if result.hand_landmarks:
                for landmarks in result.hand_landmarks:
                    # 1. DRAW SKELETON DOTS
                    for lm in landmarks:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(frame, (cx, cy), 3, (34, 211, 238), -1)

                    # 2. GESTURE LOGIC (Finger Counting)
                    fingers = []
                    # Thumb
                    if landmarks[4].x < landmarks[3].x: fingers.append(1)
                    else: fingers.append(0)
                    # 4 Fingers
                    for tip, joint in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                        if landmarks[tip].y < landmarks[joint].y: fingers.append(1)
                        else: fingers.append(0)

                    # 3. MAPPING
                    if fingers == [0, 1, 0, 0, 0]: label = "ONE / POINTING ☝️"
                    elif fingers == [0, 1, 1, 0, 0]: label = "TWO / PEACE ✌️"
                    elif fingers == [0, 1, 1, 1, 0]: label = "THREE 🤟"
                    elif fingers == [0, 1, 1, 1, 1]: label = "FOUR ✋"
                    elif fingers == [1, 1, 1, 1, 1]: label = "FIVE / HELLO 👋"
                    elif fingers == [1, 0, 0, 0, 0]: label = "THUMBS UP 👍"
                    elif fingers == [0, 0, 0, 0, 1]: label = "PINKY UP (LITTLE) 🤙"
                    
                    # 2. ALPHABET FOUNDATIONS (ASL STYLE)
                    elif fingers == [0, 0, 0, 0, 0]: label = "CLOSED FIST (A/S/E) ✊"
                    elif fingers == [1, 1, 0, 0, 0]: label = "L - SHAPE ∟"
                    elif fingers == [1, 0, 0, 0, 1]: label = "SPIDERMAN / LOVE 🤟"
                    elif fingers == [0, 1, 0, 0, 1]: label = "ROCK ON 🤘"
                    elif fingers == [1, 1, 0, 0, 1]: label = "I LOVE YOU (ASL) ❤️"
                    elif fingers == [0, 1, 1, 0, 1]: label = "W-SIGN / WATER 💧"
                    elif fingers == [1, 1, 1, 0, 0]: label = "OKAY SIGN (F-STYLE) 👌"
                    
                    # 3. SOCIAL GESTURES & COMMANDS
                    elif fingers == [1, 1, 1, 1, 0]: label = "B-SIGN (STOP) ✋"
                    elif fingers == [0, 0, 1, 1, 1]: label = "OKAY (ALT) ✅"
                    elif fingers == [0, 0, 1, 0, 0]: label = "MIDDLE FINGER (WARNING) ⚠️"
                    elif fingers == [1, 0, 1, 1, 1]: label = "CALL ME 🤙"
                    elif fingers == [0, 1, 0, 1, 1]: label = "TRI-FINGER 🔱"
                    elif fingers == [1, 0, 0, 1, 0]: label = "THUMB & RING 💍"
                    elif fingers == [1, 0, 0, 1, 1]: label = "SURF'S UP 🌊"
                    
                    # 4. DIRECTIONAL & MULTI-STATE
                    elif fingers == [0, 0, 1, 1, 0]: label = "TWO-MIDDLE BINOCULARS 👓"
                    elif fingers == [1, 1, 1, 0, 1]: label = "BIRD WING 🐦"
                    elif fingers == [0, 1, 0, 1, 0]: label = "V-GAP SIGN 🖖"
                    elif fingers == [1, 0, 1, 0, 0]: label = "THUMB-MIDDLE (SNAP) 🫰"
                    elif fingers == [0, 1, 1, 1, 0]: label = "E-FLAT 📏"
                    
                    # 5. COMPLEX COMBINATIONS (Generated for scale)
                    elif fingers == [1, 0, 1, 0, 1]: label = "TRIPLE-SPLIT 🔱"
                    elif fingers == [1, 1, 0, 1, 0]: label = "GUN SHAPE 🔫"
                    elif fingers == [0, 1, 0, 0, 1]: label = "PINKY-INDEX (DEVIL) 😈"
                    elif fingers == [1, 0, 1, 1, 0]: label = "THREE-LOW 📉"
                    elif fingers == [0, 0, 1, 0, 1]: label = "PINKY-MIDDLE ⚡"
                    elif fingers == [1, 1, 0, 1, 1]: label = "SPIDER-ALT 🕸️"
                    elif fingers == [0, 1, 1, 1, 0]: label = "FORK SIGN 🍴"
                    elif fingers == [1, 0, 1, 0, 0]: label = "SNAP PREP ✨"
                    elif fingers == [1, 1, 0, 0, 1]: label = "PHONE GESTURE 📱"
                    elif fingers == [0, 1, 0, 1, 1]: label = "TRIDENT 🔱"
                    elif fingers == [1, 1, 1, 0, 1]: label = "FLIGHT SIGN ✈️"
                    elif fingers == [0, 0, 0, 1, 1]: label = "PINKY-RING UP 🎀"
                    elif fingers == [0, 1, 1, 0, 1]: label = "M-SHAPE Ⓜ️"
                    elif fingers == [1, 1, 0, 1, 0]: label = "L-ALT 📐"
                    elif fingers == [1, 0, 0, 0, 0]: label = "APPROVE 👍"
                    elif fingers == [0, 1, 0, 0, 0]: label = "UPWARDS ⬆️"
                    elif fingers == [0, 0, 1, 0, 0]: label = "CENTERED 📍"
                    elif fingers == [0, 0, 0, 1, 0]: label = "RING FOCUS 💍"
                    elif fingers == [0, 0, 0, 0, 1]: label = "SMALL SIGN 🤏"
                    elif fingers == [1, 1, 0, 0, 0]: label = "CORNER 📐"
                    elif fingers == [1, 0, 1, 0, 0]: label = "K-SIGN 🏗️"
                    elif fingers == [1, 0, 0, 1, 0]: label = "D-ALT 💎"
                    elif fingers == [1, 0, 0, 0, 1]: label = "Y-SIGN (ASL) 🤙"
                    elif fingers == [0, 1, 1, 1, 1]: label = "B-PALM 🤚"
                    else:
                        label = "ANALYZING NEURAL PATTERN..."

            # FORCE LIVE UPDATE TO UI
            output_placeholder.markdown(f'''
                <div class="result-box">
                    <small style="color:#94a3b8">AI PREDICTION</small><br>
                    {label}
                </div>
            ''', unsafe_allow_html=True)
            
            FRAME_WINDOW.image(frame, channels="BGR")
        
        cap.release()
    else:
        output_placeholder.markdown(f'<div class="result-box"><small style="color:#94a3b8">AI PREDICTION</small><br>Offline</div>', unsafe_allow_html=True)

st.markdown(f"<br><hr><center><p style='color: #475569 !important; font-size: 12px;'>SYSTEM: NEXUS CORE | SVVV 2026 | OPERATOR: {st.session_state.user}</p></center>", unsafe_allow_html=True)