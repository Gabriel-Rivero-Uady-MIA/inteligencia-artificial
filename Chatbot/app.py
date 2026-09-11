import os

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from google import genai

MODEL = "gemini-3.6-flash"
KEY_URL = "https://aistudio.google.com/apikey"

load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("Chatbot")


def gemini_error(exc: Exception) -> str:
    text = str(exc)
    if "leaked" in text.lower():
        return (
            "This API key was reported as leaked and Google disabled it. "
            f"Create a **new** key at [{KEY_URL}]({KEY_URL}) and put it in "
            "`.env` as `GEMINI_API_KEY`."
        )
    return f"Could not call Gemini: {exc}"


def reset_chat() -> None:
    client = genai.Client(api_key=GEMINI_API_KEY)
    st.session_state.client = client
    st.session_state.chat = client.chats.create(model=MODEL)
    st.session_state.messages = []


if not GEMINI_API_KEY:
    st.error(
        f"Missing `GEMINI_API_KEY`. Create a key at [{KEY_URL}]({KEY_URL}) "
        "and put it in `.env`."
    )
    st.stop()

if "chat" not in st.session_state:
    reset_chat()

with st.sidebar:
    st.markdown(f"**Modelo:** `{MODEL}`")
    if st.button("Nuevo chat"):
        reset_chat()
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Escribe un mensaje")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                reply = response.text or ""
            except Exception as exc:
                reply = gemini_error(exc)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
