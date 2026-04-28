# Mumzworld AI-Native Intern Submission

**1. Track:** Track A: AI Engineering Intern

**2. Summary**
I built the **Mumzworld Agentic Triage System**, a multimodal logistics routing prototype designed to assist the customer support team. The system intercepts unstructured customer complaints (text and images), cross-references a local MongoDB cluster for live inventory/policy context (RAG), and utilizes a stateful LangGraph pipeline to output Pydantic-validated JSON triage payloads. It flags edge cases (e.g., medical hazards, serial return fraud, hygiene policy violations) and translates draft responses into Fusha Arabic, helping to reduce manual support bottlenecks while minimizing AI hallucination risks.

**3. Prototype Access**
- **Live Dashboard Prototype:** [https://ai-support-system-three.vercel.app/](https://ai-support-system-three.vercel.app/)
- **GitHub Repository:** [https://github.com/adityasuhane-06/AI-Support-System](https://github.com/adityasuhane-06/AI-Support-System)
- *(Setup and run instructions are located in the master `README.md` and take under 5 minutes to execute via Uvicorn/Vite).*

**4. Walkthrough Video**
- **Prototype Walkthrough (5 inputs, including uncertainty refusal):** [https://drive.google.com/file/d/1ezWB1op4_ejJpfSK7vXUS479i4gGxfwO/view?usp=sharing](https://drive.google.com/file/d/1ezWB1op4_ejJpfSK7vXUS479i4gGxfwO/view?usp=sharing)

**5. Markdown Deliverables**
- **EVALS:** Detailed 10-case rubric, scoring, and failure honesty can be found in the repository: [`EVALS.md`](https://github.com/adityasuhane-06/AI-Support-System/blob/main/EVALS.md)
- **TRADEOFFS:** Architecture scope, LangGraph vs LangChain routing, and uncertainty logic can be found in the repository: [`TRADEOFFS.md`](https://github.com/adityasuhane-06/AI-Support-System/blob/main/TRADEOFFS.md)

**6. AI Usage Note**
**Harness:** Google DeepMind's Antigravity Agent — used as a continuous pair-coding loop (not one-shot generation) across the full build: FastAPI backend, LangGraph pipeline, Pydantic schema design, MongoDB seed data, React Three Fiber UI, and Railway/Vercel deployment config.
**Models:** `gemini-2.5-flash` (primary, multimodal) → `google/gemma-3-12b-it:free` via OpenRouter (rate-limit fallback) → `glm-4.7-flash` via Z.AI (tertiary text-only fallback).
**What worked:** Agent scaffolded the LangGraph `AgentState` TypedDict and 3-tier exception handling correctly on first attempt.
**Where we overruled:** Agent suggested a deprecated OpenRouter model (`llama-3.2-11b-vision`) that returned a live 404. We manually scraped the OpenRouter `/models` API to identify the correct endpoint. We also stripped significant marketing language ("enterprise-grade", "eliminate triage latency") the agent added to the README during a full audit pass.

**7. Time Log**
- **Research & Scoping:** 1 hour (Deciding to build a structured RAG triage system to reduce incorrect refund approvals caused by AI hallucination).
- **Backend & LangGraph Pipeline:** 2.5 hours (Setting up Pydantic strict schemas, MongoDB mocked data, and the 3-Tier Cascade).
- **Frontend UI & Visualization:** 1 hour (Building the React Vite interface and wiring the API endpoints).
- **Evals & Documentation:** 1 hour (Running adversarial edge cases and documenting tradeoffs).
*(Total time: ~5.5 hours. Went slightly over due to debugging the 3-tier API cascade and rotating leaked credentials mid-build.)*
