import os

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from google import genai

MODEL = "gemini-3.6-flash"
KEY_URL = "https://aistudio.google.com/apikey"

load_dotenv(find_dotenv())

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("Chatbot")
st.caption(f"Gemini (`{MODEL}`), same client as the LLM notebook.")


def gemini_error(exc: Exception) -> str:
    text = str(exc)
    if "leaked" in text.lower():
        return (
            "This API key was reported as leaked and Google disabled it. "
            f"Create a **new** key at [{KEY_URL}]({KEY_URL}), then paste it "
            "in the sidebar or in `.env` as `GEMINI_API_KEY`."
        )
    return f"Could not call Gemini: {exc}"


def reset_chat(api_key: str) -> None:
    client = genai.Client(api_key=api_key)
    st.session_state.client = client
    st.session_state.chat = client.chats.create(model=MODEL)
    st.session_state.messages = []
    st.session_state.active_api_key = api_key


if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY") or ""

with st.sidebar:
    st.markdown(f"**Model:** `{MODEL}`")
    api_key = st.text_input(
        "GEMINI_API_KEY",
        type="password",
        key="gemini_api_key",
        help=f"Create a key at {KEY_URL}. Do not commit it.",
    )
    if st.button("New chat"):
        if api_key:
            reset_chat(api_key)
        st.rerun()

if not api_key:
    st.error(
        f"Missing `GEMINI_API_KEY`. Create a key at [{KEY_URL}]({KEY_URL}) "
        "and paste it in the sidebar, or put it in `.env`."
    )
    st.stop()

if st.session_state.get("active_api_key") != api_key:
    reset_chat(api_key)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Write a message")
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
