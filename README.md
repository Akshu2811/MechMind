# MechMind

RAG-based industrial maintenance assistant. (Description to be filled in.)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # fill in API keys / Qdrant URL
uvicorn app.main:app --reload
```

Health check: `GET /health` -> `{"status": "ok"}`
