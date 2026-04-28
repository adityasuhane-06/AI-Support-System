# Project Decisions & Architecture

This document logs the core technical and product decisions made so future agents can understand the 'why' behind the codebase.

## 1. Problem Selection
**Decision:** We chose the "Support Ticket Triage Agent" (Option B) combined with Multimodal inputs.
**Why:** It is highly practical for e-commerce, allows us to easily write rigorous automated evals (25% of the grade requirement), and clearly solves the "Uncertainty Handling" requirement (escalating to humans on low confidence). Adding the Multimodal component (images) fulfills the requirement to use 2+ advanced AI patterns.

## 2. Tech Stack Setup
**Backend:** Python with FastAPI. Fast, natively supports async, and standard for AI data engineering.
**Frontend:** React (Vite). Allows us to build a professional-looking dashboard for the final Loom demo.
**LLM SDK:** `langchain-google-genai` (Gemini API) and `langgraph`. 
**Why Gemini & LangGraph:** Gemini provides excellent native multimodality (vision), strict JSON structured output, big context window for RAG, and an accessible free tier. We are using **LangGraph** to handle the agent orchestration loop, allowing us to strictly control cycles and state between the RAG retrieval, Tool calling, and final synthesis.
**Structured Output:** `Pydantic` will be used in Python to guarantee the JSON schema produced by Gemini is strictly validated before being sent to the DB/Frontend.

## 3. Core AI Architecture
- **RAG:** Used to look up internal Mumzworld "Return Policies" (stored locally or in the DB).
- **Tool Use:** Agent will execute functions to lookup "Order Status" and "Customer VIP Status" directly from a live **MongoDB Cluster**.
- **Multimodal:** Agent will review customer-attached photos (e.g., "broken stroller wheel") to verify damage claims.
