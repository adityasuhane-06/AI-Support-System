import json

MOCK_POLICY_DOCUMENT = """
# Mumzworld Internal Support Policy Guideline

## 1. Return eligibility & Timeframes
- **Standard Return Window:** Items can be returned within 7 days of the "DELIVERED" status.
- **Exceptions:** If the item is defective, the return window extends to 14 days. Defective claims MUST be accompanied by a clear photo. If the user claims a defect but provides no photo, the agent must ask for a photo.

## 2. Condition of Items
- **Unused & Original Packaging:** To be eligible for a standard refund, items must be unused, unwashed, and in original packaging with tags intact.
- **Hygiene Products:** Under NO CIRCUMSTANCES can hygiene products be returned if the seal is broken. This includes: Breast pumps, diapers, pacifiers, bottles, potty trainers, and maternity underwear.
- **Electronics / Appliances:** Opened electronics (e.g., baby monitors, sterilizers) cannot be returned for a refund unless they are proven defective. If unopened, standard 7-day rule applies.

## 3. Refunds vs. Store Credit
- Refunds to the original payment method take 7-14 business days.
- Store Credit (Mumzworld Wallet) is instant upon item receipt at the warehouse. When offering a refund, actively suggest Store Credit as a faster alternative.

## 4. VIP Customers Priority Escalation
- If a customer's VIP status is TRUE (often based on LTV > 3000 AED), agents have the authority to waive the 7-day return limit up to 14 days for standard items to preserve loyalty.

## 5. Escalation & Safety Scenarios (MEDICAL & ANGER)
- **Medical/Health Hazards:** If a customer mentions an allergy, rash, choking hazard, injury, or any medical condition caused by a product, the AI MUST NOT process a standard return. It MUST immediately ESCALATE to the Human Safety Team.
- **High Anger / Legal Threats:** If the customer threatens legal action, calls consumer protection, or uses severe profanity, flag `requires_human_escalation` as TRUE.

## 6. Language Policy
- Support must be replied to in the same language the customer used.
- Arabic replies must be in formal, empathetic, highly polite Arabic (Fusha/MSA), not direct machine translation.

## 7. Advanced Logistics, Fraud, and Gifting
- **Gifting:** If `is_gift` is TRUE, under NO circumstances can a refund be sent to the original payment method. The AI must select `REFUND_TO_WALLET`.
- **Heavy Items (Freight):** If a line item's `weight_kg` > 5.0, it cannot be dropped off at Aramex. The AI must select `SCHEDULE_FREIGHT_PICKUP` and instruct the user to schedule a time.
- **Fraud Monitoring:** If `total_returns_count` > 3, the customer has a high return abuse rate. The AI must flag `requires_human_escalation` as TRUE.
- **Active Returns:** If `active_return_in_progress` is TRUE, the AI must NOT initiate a new return. It must select `NONE` and inform the customer their return is already processing.

## 8. International Customs & Warranties
- **International Returns (GCC):** Free returns are ONLY applicable for `country` = "UAE". If a customer's `shipping_address` -> `country` is "KSA" or elsewhere, inform them that a 50 AED cross-border customs return fee will be deducted from their refund.
- **Warranty Claims:** If a customer wishes to return an item well beyond the 14-day limit, but the item's `warranty` is > 0 months and it is still within the warranty window, classify the intent as `WARRANTY_CLAIM`. Instruct them to contact the manufacturer (like Bugaboo or Nanit) directly and that Mumzworld cannot issue a direct refund.
"""

def retrieve_policy_context(query: str) -> str:
    """
    In a real app, this would use embeddings (e.g. SentenceTransformers) and a VectorDB (Pinecone, Chroma) 
    to retrieve the relevant chunk. For this 5-hour prototype, we simulate RAG by returning the core policy doc.
    """
    return MOCK_POLICY_DOCUMENT
