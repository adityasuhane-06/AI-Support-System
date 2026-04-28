# Mumzworld AI-Native Intern Submission

**1. Track:** Track A: AI Engineering Intern

**2. Summary**
I built the **Mumzworld Agentic Triage Node**, a multimodal logistics routing prototype designed to assist the customer support team. The system intercepts unstructured customer complaints (text and images), cross-references a local MongoDB cluster for live inventory/policy context (RAG), and utilizes a stateful LangGraph pipeline to output highly deterministic, Pydantic-validated JSON triage payloads. It instantly flags edge cases (e.g., medical hazards, serial return fraud, hygiene policy violations) and translates draft responses into Fusha Arabic, helping to reduce manual support bottlenecks while minimizing AI hallucination risks.

**3. Prototype Access**
- **Live Dashboard Prototype:** [https://ai-support-system-three.vercel.app/](https://ai-support-system-three.vercel.app/)
- **GitHub Repository:** [https://github.com/adityasuhane-06/AI-Support-System](https://github.com/adityasuhane-06/AI-Support-System)
- *(Setup and run instructions are located in the master `README.md` and take under 5 minutes to execute via Uvicorn/Vite).*

**4. Walkthrough Video**
- **3-Minute Loom Walkthrough:** [https://drive.google.com/file/d/1ezWB1op4_ejJpfSK7vXUS479i4gGxfwO/view?usp=sharing](https://drive.google.com/file/d/1ezWB1op4_ejJpfSK7vXUS479i4gGxfwO/view?usp=sharing)

**5. Markdown Deliverables**
- **EVALS:** Detailed 10-input rubric, scoring, and failure honesty can be found in the repository: [`EVALS.md`](https://github.com/adityasuhane-06/AI-Support-System/blob/main/EVALS.md)
- **TRADEOFFS:** Architecture scope, LangGraph vs LangChain routing, and uncertainty logic can be found in the repository: [`TRADEOFFS.md`](https://github.com/adityasuhane-06/AI-Support-System/blob/main/TRADEOFFS.md)

**6. AI Usage Note**
I utilized **Google DeepMind's Antigravity Agent** for deep pair-programming, specifically offloading boilerplate generation for the FastAPI backend and React Three Fiber WebGL visualization. For the actual engine intelligence, I integrated `gemini-2.5-flash` natively for multimodal speed, and engineered a failover layer via OpenRouter (`google/gemma-3-12b-it:free`) to bypass upstream 429 rate limits dynamically.

**7. Time Log**
- **Research & Scoping:** 1 hour (Deciding to build a structured RAG triage node to prevent refund hallucinations).
- **Backend & LangGraph Pipeline:** 2.5 hours (Setting up Pydantic strict schemas, MongoDB mocked data, and the 3-Tier Cascade).
- **Frontend UI & Visualization:** 1 hour (Building the React Vite interface and wiring the API endpoints).
- **Evals & Documentation:** 1 hour (Running adversarial edge cases and documenting tradeoffs).
*(Total time: ~5.5 hours. Slightly over 5 hours due to rigorously testing the 3-Tier API failover cascade.)*
