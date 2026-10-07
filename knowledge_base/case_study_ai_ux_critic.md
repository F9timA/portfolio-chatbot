# Case Study: AI UX Critic

## Role
Fatima Naseer designed and built AI UX Critic end-to-end — from product concept and UX rubric design through to the engineering of the RAG pipeline, prompt design, and deployment. This was a solo project combining her UI/UX design background with hands-on AI engineering.

## What It Does
AI UX Critic is a web app that takes a UI screenshot and returns a structured usability critique grounded in real UX guidelines rather than generic AI opinions. A user uploads a screenshot, clicks "Run Critique," and receives a set of color-coded issue cards. Each card names the specific rule violated, gives a plain-language explanation of why it matters in that specific image, assigns a severity rating, locates the issue precisely, and suggests a concrete fix.

## Tech Stack
- **Gemini API (gemini-3.6-flash):** the vision-capable model that reads the screenshot and generates the critique
- **Gemini Embeddings (gemini-embedding-001):** converts text into vectors for the retrieval layer
- **ChromaDB:** local vector database storing the embedded UX knowledge base
- **Streamlit:** web UI and free hosting/deployment
- **Python:** Pillow for image handling, python-dotenv for configuration

## Key Engineering Decisions

### RAG over plain prompting
Instead of asking Gemini to critique a screenshot purely from its general knowledge, Fatima built a retrieval layer: Nielsen's 10 usability heuristics, WCAG contrast guidelines, and UX best practices were chunked, embedded, and stored in ChromaDB. Every critique first retrieves the most relevant guideline passages, then injects them into the prompt — so the output is grounded in citable standards, not just the model's opinion. This is the decision that turns the project from a simple API wrapper into a genuine AI engineering project.

### Structured JSON output over free text
Using Gemini's schema-enforced JSON mode instead of parsing free-form text meant the UI could reliably render clean cards, and meant severity, location, and fix fields were guaranteed to exist in a consistent shape every time.

### Separating "rule name" from "why it matters here"
Early testing showed the model was pasting guideline text verbatim into the critique, which made every contrast issue sound identical regardless of context. Fatima split the schema into a short `heuristic_violated` label plus a separate `explanation` field, with an explicit instruction to write unique, context-specific reasoning for each issue. This turned generic checklist output into something that reads like an actual design review.

### Severity calibrated by element role, not violation type
Initially, severity ratings were inconsistent — a tiny decorative badge could get flagged as seriously as a broken navigation bar, purely because both involved a contrast issue. Fatima rebuilt the rubric as a two-step process: the model first classifies the element's role (primary, secondary, or tertiary), and severity is then derived directly from that role. This made severity ratings consistent and defensible across very different screenshots.

### Free-tier-only stack
Every component — model, embeddings, vector database, and hosting — runs on free tiers with no credit card required, a deliberate constraint given the goal of a fast, low-cost build.

## Challenges Solved

**Model deprecation mid-build:** the initial SDK (`google-generativeai`) and the model names Fatima started with (`gemini-1.5-flash`, then `gemini-2.0-flash`) were retired partway through development. She resolved this by migrating to the current `google-genai` SDK and following the API's own error messages, which pointed to the correct current model names.

**Vague, repetitive critique output:** solved through iterative prompt engineering — testing against a batch of varied real screenshots (her own work, Dribbble shots, and live sites) and tightening instructions based on actual observed failure patterns rather than guesswork.

**Severity inconsistency:** solved by redesigning the rubric around a role-classification step rather than trying to tune individual examples one at a time.

**Deployment:** shipped to a public, live Streamlit URL, with the API key handled securely via Streamlit's platform secrets rather than committed to the repo.

## Why This Project Matters
AI UX Critic demonstrates that Fatima can go beyond calling an API — she designed a retrieval architecture, debugged real production issues (model deprecations, inconsistent outputs), and made deliberate trade-offs (JSON schema design, severity rubric design) that show engineering judgment rather than just prompt-writing. It sits at the intersection of her design expertise (she knows what a *good* usability critique should actually contain) and her growing AI engineering skillset.
