import streamlit as st
import os
from dotenv import load_dotenv
from translator import Translator, TranslatorConfig 

# 1. Load your .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Page Configuration
st.set_page_config(
    page_title="AI Multi-Language Translator",
    page_icon="🌐",
    layout="centered"
)

# 3. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Translation Settings")
    # Mapping languages to codes
    src_lang = st.selectbox("Source Language", ["English", "Hindi", "Spanish","Arabic","Korean","Japanese","Russian","Bengali","Mandarin Chinese", "French"])
    tgt_lang = st.selectbox("Target Language", ["Hindi", "English", "Spanish","Arabic","Korean","Japanese","Russian","Bengali","Mandarin Chinese", "French"], index=1)
    
    st.divider()
    #st.info("💡 Using Gemini 2.5 Flash (Stable)\nProvider: google_genai")

# 4. Initialize Translator Engine
@st.cache_resource
def get_translator_engine(source, target):
    if not api_key:
        st.error("❌ API Key not found! Please check your .env file.")
        return None
        
    try:
        # UPDATED FOR 2026: gemini-1.5-flash is retired.
        # Use gemini-2.5-flash (Stable) or gemini-3-flash-preview (Latest)
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
st.title("🤖 AI Multi-Language Translator")
st.markdown("---")

user_text = st.text_area("Enter text to translate:", placeholder="Type your text here...", height=200)
#--- Drag & Drop for Media ---


if st.button("Translate Now", type="primary"):
    if not user_text:
        st.warning("⚠️ Please enter some text.")
    elif translator:
        with st.spinner(f"AI is translating {src_lang} to {tgt_lang}..."):
            try:
                # Call the translation method in translator.py
                result = translator.translate(user_text)
                
                # Display Results
                st.success("Translation Complete!")
                st.subheader("Result:")
                st.info(result)
                
            except Exception as e:
                # Check for 404 (Retired Model) or 429 (Quota)
                err_msg = str(e)
                if "404" in err_msg:
                    st.error("🚨 Error 404: The model name is invalid or retired. Using 'gemini-2.5-flash' should fix this.")
                elif "429" in err_msg or "ResourceExhausted" in err_msg:
                    st.error("⏳ Quota Exceeded. Please wait 60 seconds (Free Tier limit).")
                else:
                    st.error(f"❌ Translation failed: {err_msg}")
    else:
        st.error("❌ Engine not initialized.")

st.markdown("---")
st.markdown("<p style='text-align: center;'>or</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📂 Drag & Drop MP3 or MP4 here", type=["mp3", "mp4"])
if uploaded_file is not None:
    # 1. Save to a temporary file locally so the backend can read it
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        temp_file_path = tmp.name

    if st.button("🚀 Translate Media"):
        with st.spinner("AI is listening/watching..."):
            try:
                # Call the new backend method
                result = translator.translate_media(temp_file_path)
                st.subheader("Translated Output:")
                st.success(result)
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                # Clean up the local temp file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
# Footer
st.markdown("---")
st.caption("Ayushi yadav:- LLM AS TRANSLATOR ")

#streamlit run frontend.py