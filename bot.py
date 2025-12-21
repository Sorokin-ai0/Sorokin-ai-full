import streamlit as st
import google.generativeai as genai

# --- 1. THE 2025 PRODUCT ENGINE ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"].strip()
        
        # We use 'rest' to ensure your Mac doesn't hit a networking wall
        genai.configure(api_key=api_key, transport='rest')
        
        # NEW 2025 MODEL ID: gemini-3-flash-preview
        # This model is faster than 1.5 and built for agentic tasks.
        model = genai.GenerativeModel(
            model_name='gemini-3-flash-preview',
            system_instruction=(
                "Your name is Sorokin AI. You are a prestigious academic mentor. "
                "Only discuss education, science, and history. "
                "Always end with a 'Sorokin Study Tip'."
            )
        )
    else:
        st.error("🛑 Security Error: Key not found in secrets.toml")
        st.stop()
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 2. THE UI ---
st.set_page_config(page_title="Sorokin AI", page_icon="🎓")
st.title("🎓 Sorokin AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 3. THE CHAT ---
if prompt := st.chat_input("Ask Sorokin AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # This is the moment of truth for the Gemini 3 engine
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Engine Error: {e}")
            st.info("Check: Is your API key from AI Studio and not Google Cloud Vertex?")