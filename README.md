# Mumzworld AI: Next-Gen Agentic Triage Platform

An enterprise-grade, omnichannel AI Customer Support platform built explicitly for **Mumzworld**. This system intercepts incoming customer support emails, cross-references internal databases natively via an autonomous LangGraph pipeline, evaluates localized edge cases (like KSA cross-border fees and local hygiene standards), evaluates physical image submissions, and drafts fully bilingual (English/Fusha Arabic) resolution strategies in real-time.

---

## ⚡ Architecture Diagram

The system operates on an asynchronous Python/React stack, utilizing a fully deterministic LangGraph pipeline to guarantee accurate enterprise grounding before consulting the model core.

```mermaid
graph TD
    %% Frontend Node
    React[React + Vite Frontend\nThree.js Dashboard]:::frontend -->|REST API / Base64| API(FastAPI Gateway Node):::backend
    
    %% API to Langgraph
    API --> Graph{LangGraph State Core}:::graph
    
    %% Langgraph Logic Flow
    Graph -->|Step 1| Regex[Regex Intent Extraction]
    Regex -->|Detects MW-XXXXX| Mongo[(MongoDB Catalog\n& VIP Profiles)]:::db
    Mongo -->|Context| RAG[RAG Local Policy Rules]
    RAG -->|Context| Gemini((Gemini 2.5 Flash\nMultimodal LLM)):::ai
    
    %% Multimodal Evaluation
    Gemini -.->|Analyses| Vision[Visual Damage/Fraud Detection]
    Vision -.-> Gemini
    
    %% Output
    Gemini -->|Strict JSON Output| Output[Structured Triage Response]
    Output --> API
    API --> React

    classDef frontend fill:#0f172a,stroke:#d946ef,stroke-width:2px,color:#fff;
    classDef backend fill:#1e293b,stroke:#3b82f6,color:#fff;
    classDef graph fill:#334155,stroke:#fff,color:#fff;
    classDef db fill:#065f46,stroke:#10b981,color:#fff;
    classDef ai fill:#312e81,stroke:#818cf8,stroke-width:2px,color:#fff;
```

---

## 🚀 The 10 Enterprise Edge Cases
The routing core natively understands deeply complex scenarios preventing hallucination and securing Mumzworld logistics. Standard "returns" are overridden if any of these conditions are met:

1. **🏥 Severe Medical & Danger Hazmat:** If a product triggers "rash", "choking", or "hospital", the system physically blocks standard refunds and forces a **Red Escalation**, routing immediately to human legal/safety teams.
2. **🚫 Serial Fraud Protection:** AI scans the User's MongoDB profile. If historical `returns > 3`, the request is flagged for Fraud Escalation inherently regardless of policy.
3. **🛠️ Hardcoded Logistics Override:** If the DB indicates `weight_kg > 5.0`, the system revokes Aramex drop-off instructions and pivots seamlessly to `SCHEDULE_FREIGHT_PICKUP`.
4. **📅 Live Warranty Constraints:** By tracking `datetime.now()` natively, an item returned after 180 days is dynamically evaluated against the catalog's `warranty: 12` integer. It will pivot intent to `WARRANTY_CLAIM` instead of rejecting it.
5. **🛃 International Cross-Border Fees:** If the database `shipping_address` registers KSA instead of UAE, the LLM intercepts with a warning regarding a 50 AED cross-border fee structure deduction.
6. **🩺 Hygiene Isolation:** Strict rejection of returns involving open breast pumps/diapers, quoting local hygiene standards directly fetched from RAG memory.
7. **🎁 Gifting Anomalies:** Identifying `is_gift: true` in the MongoDB object natively blocks credit card refunds, successfully rerouting it to a Mumzworld Wallet Credit strategy.
8. **💵 Proactive Wallet Up-selling:** If the user has a positive existing wallet balance, the AI proactively suggests returning to the Mumzworld Wallet rather than the bank, retaining platform liquidity.
9. **⏳ Double Dipping Denials:** Database flags stating `active_return: True` cause immediate interception gracefully informing the customer a return is already active.
10. **📦 Out-Of-Stock Exchange Pivots:** If a customer aggressively demands an "Exchange", but the inventory DB registers `in_stock: False`, the AI safely diffuses the aggression and pivots securely to `STORE_CREDIT`.

---

## 🎨 Premium Next-Gen UX UI

- **3D Neural Core Visualization:** The frontend leverages `@react-three/fiber` and Framer-Motion. An abstract Icosahedron wireframe acts as a visual anchor—idling in a deep slate rotation, and rapidly pulsing in Fuchsia (`#d946ef`) during Live Triage processing.
- **Multimodal Visual File Hub:** Natively converts customer photos (e.g. proof of broken strollers) into `Base64` inside the browser, passing it natively to Gemini Flash over the LLM pipeline for deep visual fraud deterrence.
- **Tailwind V4 Glassmorphism:** Operating entirely off the next-generation Tailwind 4 native CSS architecture, featuring deep blurs and a purely dark-mode hyper-minimalist palette.
- **Fusha Arabic Translation Node:** Instantly provides natively translated, colloquial, Right-To-Left structured Fusha Arabic replies alongside the English response stream to super-power omnichannel support teams.

---

## 🛠️ Installation & Setup (Local Development)

### 1. Database & Environment Configuration
Ensure your `backend/.env` file contains your native Gemini Developer API key:
```bash
GEMINI_API_KEY="AIzaSyB49lVZ......"
```

Because we use an internalized MongoDB architecture mock for the challenge, you must mathematically seed it prior to your first execution. 
```bash
cd backend
python seed_db.py
```

### 2. Booting the FastAPI Backend
Start the Uvicorn terminal (running Python 3.12).
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .env
```
👉 *You can verify server health via returning GET:* `http://localhost:8000/api/health`

### 3. Activating the React Dashboard
Open a secondary terminal process.
```bash
cd frontend
npm install
npm run dev
```
👉 *Dashboard will dynamically map to:* `http://localhost:5173`
