# Pre-Meeting Briefing Agent

An AI research agent that takes a company or person plus a meeting time and produces a one-page, source-backed briefing covering the last 30 days. Built for the Global AI Hackathon, Problem Statement 05 (Tavily track).

## Features
- Searches the last 30 days of news, launches, partnerships and leadership changes with Tavily
- Writes a concise one-page briefing with an LLM
- Cites a numbered source for every factual claim
- Puts anything it can't support under "Unverified / Unclear" instead of guessing
- Suggests questions to ask in the meeting
- Streamlit UI with a downloadable Markdown briefing, plus a CLI

## How it works
1. `researcher.py` runs three Tavily searches (latest news, launches/funding/partnerships, hires/leadership) limited to 30 days, then removes duplicate URLs.
2. `briefing.py` numbers the sources and sends them to the LLM with strict rules: use only the provided sources, cite every claim, never invent facts.
3. `llm_client.py` calls any OpenAI-compatible endpoint. It is configured for Groq, and works with a Bifrost gateway by changing `LLM_BASE_URL` and `LLM_MODEL` in `.env`.
4. `app.py` is the Streamlit interface (company/person, meeting date and time, meeting type).

## Project structure
```
pre-meeting-briefing-agent/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── src/
    ├── __init__.py
    ├── config.py
    ├── llm_client.py
    ├── researcher.py
    └── briefing.py
```

## Setup
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (never commit it):
```
TAVILY_API_KEY=your_tavily_key
LLM_API_KEY=your_groq_key
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
```

To route through Bifrost instead, point `LLM_BASE_URL` at your Bifrost gateway and set `LLM_MODEL` to the provider/model name it exposes.

## Usage
Command line:
```powershell
python -m src.briefing "Nebius" "2026-11-16 10:00"
```

Web UI:
```powershell
python -m streamlit run app.py
```

## Reliability and limits
- Only sources from the last 30 days are used.
- The model is instructed to cite every claim and never invent facts.
- Unsupported or unclear items go under "Unverified / Unclear".
- Every briefing ends with a clickable source list so the user can verify it.
- Quality depends on what Tavily finds. Very small companies or people with common names may return fewer or less relevant results.

## Authors & Contributors
- Kenneth Ansel
- Praveen ([@SauceK-DoeS](https://github.com/SauceK-DoeS))
