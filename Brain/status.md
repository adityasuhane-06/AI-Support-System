# Project Status

**Current Phase:** Execution Preparation
**Project:** AI-Native Intern Take-Home Assessment (Mumzworld)
**Chosen Track:** AI Engineering Intern
**Specific Problem:** Support Ticket Triage Agent (with Multimodal capabilities)

## High-Level Summary
We have finalized the product requirement. We are building a backend triage system that reads customer service emails (English and Arabic) and attached images, parses the intent, looks up orders via a mock tool, and consults company policies via RAG. It then uses structured output to return a bilingual draft reply or escalates to a human.

## Next Steps
1. Scaffold the React frontend and Python FastAPI backend.
2. Generate comprehensive Mock data (Orders, Customers, Policies).
3. Implement the Gemini API core inference pipeline with Pydantic structured output.
4. Build the automated Evals (`pytest`).
