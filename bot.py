import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
PAGE_TITLE = "Sorokin AI"
PAGE_ICON = "🎓"
MODEL_NAME = "gemini-3-flash-preview"
SYSTEM_INSTRUCTION = (
    "Your name is Sorokin AI. You are a prestigious academic mentor. "
    "Only discuss education, science, and history. "
    "Always end with a 'Sorokin Study Tip'."
)

# --- 1. THE 2025 PRODUCT ENGINE ---
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("🛑 Security Error: GOOGLE_API_KEY not found in secrets.toml")
        st.stop()

    api_key = st.secrets["GOOGLE_API_KEY"].strip()

    if not api_key:
        st.error("🛑 Security Error: GOOGLE_API_KEY is empty")
        st.stop()

    # We use 'rest' to ensure your Mac doesn't hit a networking wall
    genai.configure(api_key=api_key, transport='rest')

    # NEW 2025 MODEL ID: gemini-3-flash-preview
    # This model is faster than 1.5 and built for agentic tasks.
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION
    )
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 2. THE UI ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
st.title(f"{PAGE_ICON} {PAGE_TITLE}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 3. THE CHAT ---
if prompt := st.chat_input("Ask Sorokin AI..."):
    # Add user message to session
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)

            if not response.text:
                st.warning("⚠️ Received empty response from model")
            else:
                st.markdown(response.text)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text
                })
        except Exception as e:
            st.error(f"Engine Error: {e}")
            st.info("💡 Check: Is your API key from AI Studio and not Google Cloud Vertex?")