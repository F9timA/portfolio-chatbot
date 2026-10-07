"""
Chat-with-my-portfolio — a RAG chatbot recruiters can ask about Fatima's work.

Run locally:
    streamlit run app.py

Deployment: Streamlit Community Cloud. Set GEMINI_API_KEY in
.streamlit/secrets.toml locally, or in the app's "Secrets" panel on
Streamlit Cloud (never commit a real key to the repo). Get a free key
(no credit card needed) at https://aistudio.google.com/apikey
"""

import os
import streamlit as st
import chromadb
from google import genai
from google.genai import types

DB_DIR = "chroma_db"
COLLECTION_NAME = "portfolio"
TOP_K = 4  # how many chunks to retrieve per question

# Flash models are the ones covered by Google AI Studio's free tier.
# If this model name ever errors out (Google renames/retires models fairly
# often), check https://aistudio.google.com for the current free Flash model
# name and swap it in here — same fix you already made once in Project 1.
MODEL = "gemini-3.6-flash"

SYSTEM_PROMPT = """You are the AI portfolio assistant for Fatima Naseer, a UI/UX \
Designer who also builds AI-powered tools. You answer recruiters' and hiring \
managers' questions about Fatima's work, skills, and projects, using ONLY the \
context passages provided below each question.

Rules:
- Answer naturally and conversationally, like a knowledgeable colleague, not a \
robotic search engine.
- Speak about Fatima in the third person ("she designed...", "her role was...").
- Base every claim strictly on the provided context. If the context doesn't \
contain the answer, say you don't have that detail in her portfolio yet, and \
suggest what related thing you *can* tell them.
- Keep answers concise and recruiter-friendly — a few sentences to a short \
paragraph, not a wall of text, unless the question specifically asks for depth.
- Never invent metrics, dates, or facts that aren't in the context.
"""


@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path=DB_DIR)
    return client.get_collection(COLLECTION_NAME)


def get_api_key():
    # Prefer Streamlit secrets (used on Streamlit Cloud); fall back to env var for local dev.
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.environ.get("GEMINI_API_KEY")


def retrieve_context(collection, query: str, k: int = TOP_K):
    results = collection.query(query_texts=[query], n_results=k)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    return docs, metas


def build_user_message(query: str, docs: list, metas: list) -> str:
    context_block = "\n\n---\n\n".join(
        f"[Source: {meta['source']}]\n{doc}" for doc, meta in zip(docs, metas)
    )
    return f"""Context passages from Fatima's portfolio:

{context_block}

---

Recruiter's question: {query}"""


def main():
    st.set_page_config(page_title="Chat with Fatima's Portfolio", page_icon="\U0001F4AC")
    st.title("\U0001F4AC Chat with Fatima's Portfolio")
    st.caption(
        "Ask me anything about Fatima's projects, skills, or experience — "
        "I'll answer based on her real case studies and resume."
    )

    api_key = get_api_key()
    if not api_key:
        st.error(
            "No Gemini API key found. Add GEMINI_API_KEY to "
            ".streamlit/secrets.toml (locally) or the app's Secrets panel (on Streamlit Cloud). "
            "Get a free key at https://aistudio.google.com/apikey"
        )
        st.stop()

    if not os.path.isdir(DB_DIR):
        st.error(
            "Knowledge base not found. Run `python build_kb.py` locally first, "
            "then commit the chroma_db/ folder (or rebuild it on startup — see README)."
        )
        st.stop()

    collection = get_collection()
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Suggested starter questions
    if not st.session_state.messages:
        st.markdown("**Try asking:**")
        cols = st.columns(3)
        starters = [
            "What was her role in the AI UX Critic project?",
            "What's her tech stack for AI projects?",
            "Tell me about the Safar app.",
        ]
        for col, starter in zip(cols, starters):
            if col.button(starter):
                st.session_state.pending_prompt = starter

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about Fatima's work...")
    if not prompt and "pending_prompt" in st.session_state:
        prompt = st.session_state.pop("pending_prompt")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        docs, metas = retrieve_context(collection, prompt)
        user_message = build_user_message(prompt, docs, metas)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            stream = client.models.generate_content_stream(
                model=MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=600,
                ),
            )
            for chunk in stream:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "\u258c")
            placeholder.markdown(full_response)

            with st.expander("Sources used for this answer"):
                seen = set()
                for meta in metas:
                    if meta["source"] not in seen:
                        st.markdown(f"- {meta['source']}")
                        seen.add(meta["source"])

        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
