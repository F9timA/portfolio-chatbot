# Chat with My Portfolio

A RAG (Retrieval-Augmented Generation) chatbot recruiters can literally chat with —
"What was her role in the AI UX Critic project?", "What's her tech stack?", "Tell me about Safar" —
and get answers grounded in real case studies and resume content, not hallucinated ones.

## How it works

1. **Knowledge base** (`knowledge_base/*.md`): your resume + case studies, written in plain markdown.
2. **`build_kb.py`**: chunks those markdown files and embeds them into a local ChromaDB vector store
   (`chroma_db/`), using ChromaDB's free built-in embedding model — no API key needed for this step.
3. **`app.py`**: a Streamlit chat UI. When a recruiter asks a question, it:
   - embeds the question and retrieves the most relevant chunks from `chroma_db/`
   - sends those chunks + the question to the Gemini API (free tier, via Google AI Studio)
   - streams back a grounded answer, and shows which case studies it pulled from

## Run it locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build the knowledge base (run once, and again any time you edit knowledge_base/*.md)
python build_kb.py

# 3. Add your Gemini API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml and paste your real key
# (get one free, no credit card, at https://aistudio.google.com/apikey)

# 4. Run the app
streamlit run app.py
```

Open the local URL Streamlit prints (usually http://localhost:8501).

## Editing your content

Everything the bot knows lives in `knowledge_base/`:

- `resume.md` — your resume, structured
- `case_study_ai_ux_critic.md` — your flagship AI project
- `case_study_safar.md` — **drafted for you, please review** — fill in real details
  (timeline, solo vs. team, the hardest problem you solved, whether it's shipped)
- `case_study_design_projects.md` — **drafted for you, please review** — same idea

Edit any `.md` file, then re-run `python build_kb.py` to rebuild the vector store before
you deploy or test again. The bot can only answer from what's actually written in these files —
if something's missing, add it here rather than hoping the model "knows" it.

## Deploying to Streamlit Community Cloud

1. Push this whole folder to a GitHub repo (public or private).
   - `chroma_db/` is small at this scale — commit it too, so the app doesn't need to
     rebuild the vector store on every deploy. If you prefer, you can instead call
     `build_kb.main()` once at app startup — but that's unnecessary complexity for ~30 chunks.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in, click "New app."
3. Point it at your repo, branch `main`, main file path `app.py`.
4. In the app's **Settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-real-key"
   ```
5. Deploy. You'll get a public URL like `https://your-app-name.streamlit.app` —
   put that link on your portfolio site or resume.

## Notes

- **Model:** the app uses `gemini-2.5-flash` by default — one of the models covered
  by Google AI Studio's free tier (no credit card needed). If Google retires this
  model name later (they do this periodically — you hit the same thing in Project 1),
  check https://aistudio.google.com for the current free Flash model name and update
  `MODEL` in `app.py`.
- **Cost:** genuinely free for this use case. The free tier covers Flash models with
  daily request limits generous enough for a portfolio demo (not unlimited — if the
  link goes viral you could hit the daily cap, but that's a good problem to have).
- **Scaling the knowledge base:** if you add many more case studies later, ChromaDB
  and this chunking approach will still work fine well beyond this size — no changes needed.
