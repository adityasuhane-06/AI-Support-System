# Mumzworld AI-Native Intern: Support Triage Agent

This is my submission for the **AI Engineering Intern** track. I built a Multimodal Support Ticket Triage Agent designed to streamline the Level-3 customer service at Mumzworld by identifying return intent, automatically handling cross-reference checks, and detecting when to escalate complex or unsafe matters to human supervisors.

## 1. Setup Instructions (Running in under 5 minutes)

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend Setup (FastAPI + LangGraph)
1. Navigate to the backend: `cd backend`
2. Create virtual environment: `python -m venv venv`
3. Activate it: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt` *(Note: Since I used dynamic commands, make sure you pip install fastapi uvicorn google-genai pymongo[srv] pydantic pytest python-dotenv langgraph langchain-google-genai langchain-core)*
5. Ensure your `.env` file matches the one provided (contains `GEMINI_API_KEY` and `MONGO_URI`).
6. Spin up the orchestrator: `uvicorn main:app --reload`

### Frontend Setup (React/Vite)
1. Open a new terminal.
2. Navigate to the frontend: `cd frontend`
3. Install packages: `npm install`
4. Start the dashboard: `npm run dev`

You can now open `http://localhost:5173` and paste customer emails to test the Triage Agent!

## 2. Evals & Proof of Capability (The 25% Grade)

Rigorous testing was paramount. I created a programmatic testing suite `backend/tests/test_evals.py` testing the rigidness of the uncertainty handling bounds. 

**My rubric targets the following edge cases:**
1. **Medical Hazard Escalation:** An email complaining about "baby getting a rash" correctly triggers `requires_human_escalation: true`.
2. **Hygiene Return Rejection (RAG Check):** An attempt to return an "opened breast pump" bypasses standard refund logic because the RAG policy context strictly forbids it.
3. **Multimodal Discrepancy:** If customer email claims a "snapped stroller wheel" but the input vision description describes an intact wheel, the system halts auto-processing and escalates.
4. **Unknown Tool Lookups (Uncertainty Handling):** If an order ID isn't found in the mock Database, the AI correctly refuses to process ("I don't know") rather than hallucinating an order status.
5. **VIP Exception Handling:** A customer attempting a return outside the 7-day window is normally rejected, but if the MongoDB tool reports their `lifetime_value_aed` > 3000 (VIP Platinum), the LLM auto-bends the rule to 14-days based on policy.

## 3. Tradeoffs & Architecture

**Problem Selection:** I rejected the "Gift Finder" because judging whether an AI gives a "good gift recommendation" is heavily subjective and extremely difficult to write rigorous programmatic Evals for. I selected the "Support Ticket Triage" because it allowed me to demonstrate extreme engineering precision through JSON validation (`Pydantic`), live database interactions (`Tool Calling`), rule enforcement (`RAG`), and edge-case handling (`State Graph Routing`).

**Architecture Choice:** I utilized **LangGraph** rather than raw LLM calls. A directed state graph allowed me to compartmentalize responsibilities (Extraction -> DB Tool -> Policy RAG -> Synthesis) making it inherently safer and easier to debug when outputs miss the schema.

**Uncertainty Handling:** My implementation forces the LLM's `temperature` to 0.1 for high determinism. Instead of hoping the model knows its limits, the LangGraph explicitly routes any missing variables or safety keywords via an `Escalation` override.

**What I cut/Would build next:** I mocked the Multimodal Vision step as text-descriptions to keep the payload size small for speed. Next, I would inject base64 image strings directly into Gemini. Furthermore, instead of static Markdown RAG, I would hook it up to an actual Pinecone Vector DB for semantic searching across a vast Mumzworld Wiki.

## 4. Tooling Profile 

- **Primary Agent Framework:** LangGraph
- **LLM Gateway:** `google-genai` (Gemini 1.5 Flash). Chosen for blistering fast structured outputs and native multimodal context windows perfect for e-commerce parsing.
- **Agent Environment:** The AI pair-programming assistant "Antigravity" was utilized globally to scaffold React code, build the `Pydantic` validation infrastructure, and generate comprehensive fake datasets spanning 150+ realistic Mumzworld items using the `faker` library, injected directly into a MongoDB cluster.
- **Overrides:** The AI was strictly guided via user-directed Architecture flows to ensure precise file layouts and MongoDB integrations were met.
