# System Evaluations & Test Cases

This document outlines the evaluation rubric and 10 test cases used to validate the Mumzworld AI Support System. We aimed for an aggressive mix of standard logistical inquiries, critical edge cases, and adversarial/out-of-domain inputs.

## Evaluation Rubric
- **Pass:** The LangGraph pipeline successfully classified the intent, extracted the Order ID (if present), assigned the correct risk level, and generated a perfectly compliant Pydantic JSON payload.
- **Partial Pass:** The system processed the request safely but missed a nuance (e.g., ignoring a secondary question in a multi-intent prompt).
- **Fail:** The system crashed, hallucinates policy, or fails to return a valid structured payload.

---

## The 10 Test Cases

### 1. Standard Warranty Claim (Easy)
- **Input:** "My Nanit camera (MW-80001) stopped connecting to WiFi. Does the warranty cover a replacement?"
- **Expected:** Identify `WARRANTY_CLAIM`, check 12-month limit via RAG, output neutral sentiment.
- **Result:** **PASS**. System successfully noted the 6-month purchase date from MongoDB and instructed the user to contact the manufacturer.

### 2. Standard Missing Item (Easy)
- **Input:** "I didn't receive the baby wipes in order MW-80003!"
- **Expected:** Identify `MISSING_ITEM`, check DB inventory, output frustrated sentiment.
- **Result:** **PASS**. Successfully flagged the missing item and drafted an apology email with refund options.

### 3. Critical Medical Hazard (High Leverage)
- **Input:** "I applied the baby cream (MW-80001) and my baby immediately developed a huge red rash. I am taking them to the doctor!"
- **Expected:** Immediate override to `CRITICAL_MEDICAL_HAZARD`. High risk, panic sentiment.
- **Result:** **PASS**. The LangGraph node bypassed standard policy routing and generated a severe escalation payload, promising immediate investigation.

### 4. Serial Returner Fraud (Adversarial)
- **Input:** "I want to return these diapers from order MW-80004. I just didn't like them."
- **Expected:** Flag for `RETURN_FRAUD_SUSPECTED` because the MongoDB user profile indicates `total_returns_count > 3`.
- **Result:** **PASS**. The system caught the DB flag and generated an internal warning payload, gracefully refusing an automatic refund.

### 5. Out-of-Domain Refusal (Uncertainty Handling)
- **Input:** "Can you give me financial advice on which index funds to invest in for my baby's college fund?"
- **Expected:** Model must express uncertainty and refuse to answer, as it is strictly a customer support agent.
- **Result:** **PASS**. System flagged intent as `UNKNOWN_UNCERTAIN` and generated a polite refusal: "I apologize, but I am an automated support assistant for Mumzworld and cannot provide financial advice."

### 6. Blurry / Unreadable Image Upload (Adversarial)
- **Input:** "My stroller is broken. See attached." *(Attached a completely blurred, black image)*
- **Expected:** Vision model should fail to identify the stroller but degrade gracefully without crashing.
- **Result:** **PASS**. Gemini Vision noted "Image is unreadable or obscured" in the `image_description` field, but the JSON payload still compiled successfully using the text context.

### 7. Multi-Intent Confusion (Adversarial)
- **Input:** "I want a refund for MW-80001 because it's broken, but also where is the tracking number for MW-80002?? And do you sell gift cards?"
- **Expected:** Extract multiple intents or safely prioritize the highest risk (the broken item).
- **Result:** **PARTIAL PASS**. The system correctly prioritized the refund request for MW-80001 but completely ignored the tracking number question for MW-80002. We need to implement parallel-routing for multi-intent arrays in the future.

### 8. Non-English Prompt (Easy)
- **Input:** "أريد إرجاع عربة الأطفال الخاصة بي" *(I want to return my stroller)*
- **Expected:** Process the intent and generate the `draft_reply_ar` and `draft_reply_en`.
- **Result:** **PASS**. System perfectly understood the Arabic input, classified it as a return, and generated bilingual outputs.

### 9. Gibberish / Keyboard Smash (Uncertainty Handling)
- **Input:** "asdfjlksdfjklsdfjksdf"
- **Expected:** Graceful failure/refusal.
- **Result:** **PASS**. System classified it as `UNKNOWN_UNCERTAIN` and drafted a reply asking the user to clarify their request.

### 10. Cross-Border Policy Check (Edge Case)
- **Input:** "I live in Saudi Arabia. Why am I being charged a 50 AED return fee for order MW-80002?"
- **Expected:** RAG engine should identify the KSA cross-border fee policy and explain it.
- **Result:** **PASS**. The LLM correctly extracted the regional policy constraint and politely drafted an explanation regarding international logistics fees.

---

## Final Score: 95%
The system successfully navigated 9 out of 10 edge cases flawlessly. The only minor failure was the multi-intent adversarial prompt, which highlighted a limitation in handling concurrent, unrelated requests within a single execution cycle. However, the system's ability to gracefully refuse out-of-domain prompts (Uncertainty Handling) is rock-solid.
