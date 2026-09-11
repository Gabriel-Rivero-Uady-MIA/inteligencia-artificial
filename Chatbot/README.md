# Chatbot

A Streamlit chat UI that talks to **Gemini**, using the same client as
`LLMs/Notebooks/04 LLM Gemini API.ipynb`: `google-genai`, a `.env` key,
and `gemini-3.6-flash`.

## Setup

```bash
cd Chatbot
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
cd Chatbot
python3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and paste a **new** key from
[Google AI Studio](https://aistudio.google.com/apikey):

```
GEMINI_API_KEY=your_key_here
```

You can also paste the key in the sidebar. Do not commit `.env`. Later
sessions: activate the venv again, then run the app. Deactivate with
`deactivate`.

If Gemini returns **403 / leaked**, that key is already public (for
example committed in git). Google will not accept it again: create a
fresh key, revoke the old one in AI Studio, and put only the new key in
`.env`.

## Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Type in the chat box; Gemini
answers with the conversation history kept in the session. **New chat**
in the sidebar starts over. Stop the server with `Ctrl+C`.
