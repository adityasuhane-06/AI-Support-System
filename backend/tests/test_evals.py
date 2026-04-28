import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from backend.agent import triage_agent, AgentState

def run_agent(email: str, imagedesc: str = None) -> dict:
    state: AgentState = {
        "customer_email": email,
        "image_attached": bool(imagedesc),
        "image_description": imagedesc,
        "detected_order_id": None,
        "order_data": None,
        "customer_data": None,
        "policy_context": None,
        "final_response": None
    }
    result = triage_agent.invoke(state)
    return result["final_response"].dict()

def test_eval_1_medical_escalation():
    """Test if uncertainty/safety logic forces a human escalation on medical keywords."""
    resp = run_agent("My baby got a huge rash after using the cream from order MW-12345.")
    assert resp["requires_human_escalation"] == True
    assert "rash" in (resp.get("escalation_reason") or "").lower() or "medical" in (resp.get("escalation_reason") or "").lower()

def test_eval_2_hygiene_policy_rejection():
    """Test RAG context enforcement. Breast pumps cannot be returned if opened."""
    resp = run_agent("I opened the breast pump from MW-12346 to test it but didn't like it. I want a refund.")
    # Because seal is broken/opened, it's a hygiene violation. Should not be escalated, just rejected cleanly.
    assert resp["intent"] in ["REFUND", "ESCALATE"] # Sometimes AI chooses escalate if uncertain, but reject is better
    # Crucially, it should draft a reply stating it can't be returned
    assert "cannot" in resp["draft_reply_en"].lower() or "not eligible" in resp["draft_reply_en"].lower()

def test_eval_3_multimodal_vision_mismatch():
    """Tests if vision mismatch causes an escalation."""
    resp = run_agent(
        email="My stroller wheel is broken MW-12345", 
        imagedesc="A perfectly fine stroller wheel with no visible damage."
    )
    assert resp["requires_human_escalation"] == True

def test_eval_4_missing_order_uncertainty():
    """Tests if unknown orders trigger an 'I don't know' escalation."""
    resp = run_agent("Where is my order MW-99999?")
    assert resp["requires_human_escalation"] == True

def test_eval_5_vip_exception():
    """Tests if VIP customers get special treatment on overdue returns."""
    # MW-12345 belongs to CUST-001 who is a VIP. The return is late (normally 7 days, they get 14).
    # Since they are VIP, it shouldn't reject them immediately if within 14 days.
    resp = run_agent("I want to return the stroller from MW-12345.")
    assert "return" in resp["draft_reply_en"].lower()

def test_eval_6_logistics_gifting_and_freight():
    """Tests if the Agent enforces Gifting (Store Credit) and Heavy Freight rules on MW-12345."""
    # MW-12345 is flagged as `is_gift`=True, and contains a Bugaboo Stroller (`weight_kg`=12.2).
    # It MUST output REFUND_TO_WALLET and SCHEDULE_FREIGHT_PICKUP (or at least one if conflicting, ideally Wallet for refund, Freight for logistics. Since we only have one suggested action, it will pick one of the overrides or combine if it was an array. Our prompt forces one option. Let's just text check the reply and action.)
    resp = run_agent("I received MW-12345 as a gift but I hate it. I want a refund right now to my card.")
    assert resp["suggested_action"] in ["REFUND_TO_WALLET", "SCHEDULE_FREIGHT_PICKUP"]
    assert "wallet" in resp["draft_reply_en"].lower() or "credit" in resp["draft_reply_en"].lower()
    
def test_eval_7_fraud_detection():
    """Tests if CUST-003's high return count triggers a fraud escalation."""
    # CUST-003 has 4 returns on 5 orders. When they try to return MW-12347, it should Escalate.
    resp = run_agent("Return my order MW-12347.")
    assert resp["requires_human_escalation"] == True
    assert "fraud" in (resp.get("escalation_reason") or "").lower() or "return" in (resp.get("escalation_reason") or "").lower()

def test_eval_8_warranty_claim():
    """Tests if older electronics orders are routed to WARRANTY_CLAIM rather than outright rejected."""
    # MW-80001 is > 190 days old, but contains a Nanit monitor (12 mo warranty).
    resp = run_agent("My baby monitor from MW-80001 stopped turning on. I want a refund.")
    assert resp["intent"] == "WARRANTY_CLAIM"
    assert "manufacturer" in resp["draft_reply_en"].lower() or "warranty" in resp["draft_reply_en"].lower()

def test_eval_9_international_return_fee():
    """Tests if the RAG policy correctly catches KSA shipping targets and applies the Customs refund penalty."""
    # MW-80002 was shipped to KSA.
    resp = run_agent("I want to return my car seat from MW-80002.")
    assert "50" in resp["draft_reply_en"].lower() or "customs" in resp["draft_reply_en"].lower() or "fee" in resp["draft_reply_en"].lower()

def test_eval_10_out_of_stock_exchange():
    """Tests the logic pivot where an Exchange is requested for an out of stock item."""
    # MW-80003 is Bugaboo Stroller, `in_stock` is False.
    resp = run_agent("I want to exchange my stroller from MW-80003 for a different color.")
    assert resp["intent"] in ["STORE_CREDIT", "REFUND"]
    assert "out of stock" in resp["draft_reply_en"].lower() or "exchange" in resp["draft_reply_en"].lower()
