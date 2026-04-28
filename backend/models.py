from pydantic import BaseModel, Field
from typing import Optional

class TriageResponse(BaseModel):
    intent: str = Field(
        description="The primary intent of the customer: REFUND, EXCHANGE, STORE_CREDIT, STATUS_CHECK, WARRANTY_CLAIM, or ESCALATE"
    )
    confidence_score: float = Field(
        description="Confidence out of 1.0 in this intent classification."
    )
    suggested_action: str = Field(
        description="The precise logistics action to take: REFUND_TO_ORIGINAL_PAYMENT, REFUND_TO_WALLET, SCHEDULE_FREIGHT_PICKUP, STANDARD_ARAMEX_DROP, or NONE."
    )
    requires_human_escalation: bool = Field(
        description="Set to true if there is a complex issue, medical issue, anger, or ambiguity."
    )
    escalation_reason: Optional[str] = Field(
        description="If requires_human_escalation is true, explain why."
    )
    draft_reply_en: Optional[str] = Field(
        description="Draft reply to the customer in English."
    )
    draft_reply_ar: Optional[str] = Field(
        description="Draft reply to the customer perfectly translated in Arabic. Read naturally and natively, not like a machine translation."
    )
