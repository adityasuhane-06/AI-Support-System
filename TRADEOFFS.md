# Tradeoffs & Architectural Decisions

This document outlines the engineering decisions, rejected scopes, and future roadmap for the Mumzworld AI Support System, as required by the grading rubric.

## 1. Problem Selection: Why Triage?
We chose **Customer Support Triage & Logistics Routing** because it is a real, high-frequency operational bottleneck for e-commerce companies.
- **What we rejected:** We initially considered building an AI chatbot that talks directly to customers. We rejected this because autonomous LLM chatbots in e-commerce are prone to hallucinating return policies and authorizing incorrect refunds, which creates massive financial liability. 
- **Why Triage is better:** By building a "Triage System" that sits *behind* the scenes, the AI does the heavy lifting of extracting order IDs, checking MongoDB policies, and determining risk, but it ultimately hands a strictly structured JSON payload to a human agent for 1-click execution. This reduces errors without replacing the human in the loop.

## 2. Model & Architecture Choices
- **LangGraph over standard LangChain:** We chose LangGraph because customer support requires cyclic state management. If the AI realizes it's missing an Order ID, a standard chain breaks. LangGraph allows us to dynamically loop back to previous nodes or route to a human safely.
- **Pydantic Structured Outputs:** We forced all LLMs to adhere to a `TriageResponse` Pydantic schema. We traded off LLM "creativity" in exchange for deterministic JSON that a frontend or API can reliably parse without crashing.
- **The 3-Tier Cascade (Gemini -> OpenRouter -> Z.AI):** We chose Google Gemini 2.5 Flash as the primary model because of its native multimodal (vision) capabilities. However, because free tiers often hit 429 Rate Limits, we engineered a 3-Tier cascade. If Gemini fails, it routes to Gemma 3 Vision on OpenRouter. If that fails, it routes to Z.AI. 

## 3. Handling Uncertainty
Does the model know what it does not know? **Yes.**
We explicitly built an `UNKNOWN_UNCERTAIN` intent flag into the Pydantic schema. If a user asks for financial advice, complains about the weather, or types gibberish, the model is strictly instructed to flag the payload as uncertain, set `requires_human_escalation = True`, and gracefully refuse to answer. (See Test Case #5 and #9 in EVALS.md).

## 4. What We Cut (Scope Reductions)
- **Direct Email Integrations:** We originally planned to wire the FastAPI backend directly into an IMAP/SMTP server to physically intercept real emails. We cut this because configuring OAuth for Gmail/Outlook was too complex for a 5-minute setup requirement. Instead, we built a React dashboard to simulate the incoming email payload.
- **Parallel Multi-Intent Routing:** Currently, if a user has two totally different issues in one email, the system focuses on the highest-risk issue. We cut parallel multi-thread execution to save on token costs.

## 5. What We Would Build Next
- **Automated Fulfillment API Hooks:** Once the human agent approves the JSON payload, we would wire the backend to directly hit Shopify/Magento APIs to physically process the refund or generate the return shipping label automatically.
- **Agentic Workflow Triggers:** Allow the LangGraph agent to dynamically query external carrier APIs (e.g., FedEx, Aramex) to fetch real-time tracking data if the customer asks "Where is my order?".
