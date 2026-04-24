import streamlit as st
import database as db
import time

st.set_page_config(page_title="NEXUS AI", page_icon="⚡", layout="wide")

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

# --- THE HIGH-CONTRAST NEON CSS ---
st.markdown("""
    <style>
    /* 1. Background & Base Text */
    .stApp { background: #020617; }
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    
    /* 2. Primary Buttons (Access, Register, Launch) */
    .stButton > button {
        background: linear-gradient(90deg, #06b6d4, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3) !important;
    }
    
    
    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.6) !important;
        transform: scale(1.02);
        color: #ffffff !important;
    }

    /* 3. Input Field Visibility */
    input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }

    /* 4. Glassmorphism Card Fix */
    [data-testid="stElementContainer"] div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 2px solid #334155 !important;
        border-radius: 20px !important;
        padding: 25px !important;
    }

    .hero-title {
        font-size: 55px; font-weight: 900; text-align: center;
        background: linear-gradient(to right, #22d3ee, #c084fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .stImage img {
         filter: drop-shadow(0 0 10px rgba(34, 211, 238, 0.4));
         margin-bottom: 10px;
}
    /* --- SIDEBAR MATCHING UI --- */
    [data-testid="stSidebar"] {
        background-color: #020617 !important; /* Matches main background */
        border-right: 1px solid rgba(34, 211, 238, 0.2); /* Neon Cyan subtle border */
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }

    /* Sidebar Text & Headers */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #22d3ee !important; /* Neon Cyan for Sidebar Headers */
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Logout Button */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(239, 68, 68, 0.1) !important; /* Subtle red for logout */
        border: 1px solid #ef4444 !important;
        color: #ef4444 !important;
        font-size: 12px !important;
        transition: 0.3s;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #ef4444 !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.4) !important;
    }
    
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Optional: If 'app' is still showing, this targets the very top list */
    [data-testid="stSidebarNav"] ul {
        display: none !important;
    }

    .card-desc { color: #94a3b8 !important; font-size: 14px; text-align: center; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def main():
    if not st.session_state.logged_in:
        # --- LOGIN SCREEN ---
        st.markdown("<style>[data-testid=\"stSidebar\"] {display: none;}</style>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>NEXUS AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Beyond Boundaries: Multimodal Translation</p>", unsafe_allow_html=True)

        _, col2, _ = st.columns([1, 1.8, 1])
        with col2:
            with st.container(border=True):
                mode = st.tabs(["🔒 Secure Login", "✨ Create Account"])
                with mode[0]:
                    u = st.text_input("Username", key="l_user")
                    p = st.text_input("Password", type="password", key="l_pw")
                    if st.button("ACCESS DASHBOARD →", use_container_width=True):
                        if db.verify_user(u, p):
                            st.session_state.logged_in = True
                            st.session_state.user = u
                            st.rerun()
                        else:
                            st.error("Invalid Username or Password")
                with mode[1]:
                    nu = st.text_input("New Username", key="s_user")
                    np = st.text_input("New Password", type="password", key="s_pw")
                    if st.button("REGISTER ACCOUNT NOW", use_container_width=True):
                        if db.add_user(nu, np):
                            st.success("Account Ready! Switch to Login.")
                        else:
                            st.error("Username already taken.")

    else:
        # --- DASHBOARD SCREEN ---
        st.sidebar.markdown(f"### 👤 User: {st.session_state.user}")
        if st.sidebar.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.rerun()

        st.markdown("<h2 style='text-align: center;'>AI Command Center</h2>", unsafe_allow_html=True)
        st.write("")

        c1, c2, c3 = st.columns(3)
       # --- DASHBOARD VIEW ---

        # CARD 1: TRANSLATOR
        with c1:
            with st.container(border=True):
                st.image("https://cdn-icons-png.flaticon.com/512/3898/3898082.png", width=80) # Modern Global Icon
                st.markdown("### Translator")
                st.markdown("<p class='card-desc'>Text, MP3, & MP4 Translation</p>", unsafe_allow_html=True)
                if st.button("LAUNCH TOOL", key="btn1", use_container_width=True):
                    st.switch_page("pages/frontend.py")

        # CARD 2: SIGN BRIDGE
        with c2:
            with st.container(border=True):
                # New 3D Gesture Icon
                st.image("https://cdn-icons-png.flaticon.com/512/4813/4813352.png", width=80)
                st.markdown("### Sign Bridge")
                st.markdown("<p class='card-desc'>Gestures to Text in Real-time</p>", unsafe_allow_html=True)
                if st.button("LAUNCH TOOL", key="btn2", use_container_width=True):
                    st.switch_page("pages/Sign_Language.py")

        # CARD 3: ENTERPRISE
        with c3:
            with st.container(border=True):
                # New Abstract Corporate/Doc Icon
                st.image("https://cdn-icons-png.flaticon.com/512/10061/10061730.png", width=80)
                st.markdown("### Enterprise")
                st.markdown("<p class='card-desc'>Doc translation with layout</p>", unsafe_allow_html=True)
                if st.button("LAUNCH TOOL", key="btn3", use_container_width=True):
                    st.switch_page("pages/Enterprise.py")
if __name__ == "__main__":
    main()