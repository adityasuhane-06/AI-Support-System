# ⚙️ Mumzworld Triage AI: API Backbone

This directory contains the primary deterministic intelligence layer for the Agentic Triage Platform. Designed intrinsically as a stateless microservice, this backend intercepts raw API requests, injects contextual grounding from internal databases, and orchestrates Google's **Gemini 2.5 Flash** natively using a strict **LangGraph** flow geometry.

## 🧱 Architecture Map

The backend prevents LLM hallucinations by never directly answering a customer query without systematically loading context first. The flow geometry defined in `agent.py` dictates:

1. **`node_extract_intent`**: Parses the raw incoming email to extract UUIDs/Order boundaries (e.g. `MW-XXXXX`).
2. **`node_tool_db_lookup`**: Natively cross-references internal `pymongo` mock states (`database.py`) to scrape VIP return histories, freight weights, and gift designations.
3. **`node_rag_policy_lookup`**: Asynchronously intercepts static organizational policies ensuring up-to-date compliance (e.g. Hygiene isolation vectors).
4. **`node_synthesize_response`**: Feeds the aggregated payload natively into Gemini via `ChatGoogleGenerativeAI` using strict Pydantic `TriageResponse` schemas.

## 🧪 Edge Case Verification Suite
Because this pipeline handles high-risk financial processing rules, it includes an aggressive deterministic testing suite. The tests natively trigger the 10 Edge Cases without human input to guarantee architectural integrity.

**To run the validation protocol:**
```bash
python -m pytest tests/test_evals.py -v
```

## 🛠️ Required Setup 
Ensure `GEMINI_API_KEY` is isolated securely within your `.env` target before running.

1. **Seed the isolated Database:** (This mathematically structures the required evaluation criteria)
```bash
python seed_db.py
```

2. **Boot the Uvicorn Engine:**
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .env
```
