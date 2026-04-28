import os
import re
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from models import TriageResponse
from database import get_order_details, get_customer_details
from rag_policy import retrieve_policy_context

# [PRIMARY TIER] Google Gemini API (Multimodal)
llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    api_key=os.getenv("GEMINI_API_KEY")
)
structured_gemini = llm_gemini.with_structured_output(TriageResponse)

# [SECONDARY TIER] OpenRouter Cloud (Multimodal Fallback)
llm_openrouter = ChatOpenAI(
    model="google/gemini-2.5-flash:free", # Explicit free vision model guarantee
    temperature=0.1,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
structured_openrouter = llm_openrouter.with_structured_output(TriageResponse)

# [TERTIARY TIER] Z.AI Engine (Text-Only Fallback)
llm_zai = ChatOpenAI(
    model="glm-4.7-flash",
    temperature=0.1,
    api_key=os.getenv("ZAI_API_KEY"),
    base_url="https://api.z.ai/api/paas/v4/"
)
structured_zai = llm_zai.with_structured_output(TriageResponse)

# Define our Agent's State (Memory during a single execution)
class AgentState(TypedDict):
    customer_email: str
    image_attached: bool
    image_description: Optional[str]
    image_base64: Optional[str]
    detected_order_id: Optional[str]
    order_data: Optional[dict]
    customer_data: Optional[dict]
    policy_context: Optional[str]
    final_response: Optional[TriageResponse]

# ---------------------------------------------------------
# GRAPH NODES (The actions our agent takes)
# ---------------------------------------------------------

def node_extract_intent(state: AgentState):
    """Scan the email to look for Order IDs (MW-XXXXX) to fetch context before generating a reply."""
    email = state["customer_email"]
    
    # Simple regex to find order IDs like MW-12345
    match = re.search(r'MW-\d{5}', email)
    if match:
        state["detected_order_id"] = match.group(0)
    
    return state

def node_tool_db_lookup(state: AgentState):
    """If an order ID was found, query the MongoDB tools."""
    order_id = state.get("detected_order_id")
    if order_id:
        order_details = get_order_details(order_id)
        if order_details:
            state["order_data"] = order_details
            # If we got the order, let's grab the customer profile too
            cust_id = order_details.get("customer_id")
            if cust_id:
                state["customer_data"] = get_customer_details(cust_id)
                
    return state

def node_rag_policy_lookup(state: AgentState):
    """Retrieve internal return and escalation policies."""
    # In a full app, we'd embed the email and search a vector DB.
    # Here, we fetch the comprehensive Mumzworld support guideline document.
    state["policy_context"] = retrieve_policy_context(state["customer_email"])
    return state

def node_vision_assessment(state: AgentState):
    """(Simulated vision node for now, standard text implementation)."""
    # In full reality, we'd pass the base64 image array to Gemini.
    # For this graph, if image_description was injected by the frontend API call, keep it.
    pass

def node_synthesize_response(state: AgentState):
    """The core intelligence. Feeds all collected context into the LLM with a massive, rigorous system prompt."""
    
    import datetime
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    system_prompt = f"""
You are the elite Level 3 Customer Support Agent AI for Mumzworld, the largest e-commerce platform for mothers in the Middle East.
Your job is to read customer emails, cross-reference their database records, strictly adhere to Mumzworld policies, and output a structured JSON response.

# CONTEXT RETRIEVED FOR THIS TICKET:
- User Email: "{state['customer_email']}"
- Uploaded Image Description (if any): "{state.get('image_description', 'No image attached')}"
- Database Order Record: {state.get('order_data', 'Order not found or not provided')}
- Customer VIP Profile: {state.get('customer_data', 'Unknown')}
- Relevant Mumzworld Policies: \n{state.get('policy_context')}
- CURRENT SERVER SYSTEM DATE: {today}

# CRITICAL DIRECTIVES & SCENARIO HANDLING:

1. **GROUNDING & UNCERTAINTY (DO NOT HALLUCINATE)**
   - If the customer asks about an order status, but `Order Record` is "not found", you MUST set `requires_human_escalation` to True and explain that you cannot find the order. Do NOT makeup a shipping status.
   - If a customer asks a complex question about product compatibility, you MUST say "I don't know" or escalate. Do not guess safety information.

2. **COMPLEX SCENARIOS (SAFETY & MEDICAL FIRST)**
   - **Hazard:** Customer mentions "choking", "rash", "allergy", "hospital", or "danger". Action: `requires_human_escalation` MUST be True. Intent = ESCALATE. 
   - **Anger:** Customer is aggressively angry, threatening to sue, or using heavy profanity. Action: `requires_human_escalation` MUST be True. Intent = ESCALATE.
   - **Hygiene Breach:** Customer wants to return an open hygiene item (Breast pump, diapers). Consult policy context. REJECT the refund politely. Suggest no alternatives. Action = `NONE`.
   
3. **ADVANCED E-COMMERCE LOGISTICS & EDGE CASES (THE NEW RULES)**
   - **Gifting:** Look at the `Order Record`. If `is_gift` is True, you CANNOT refund their credit card. Provide `suggested_action` = 'REFUND_TO_WALLET'. Inform the customer the Store Credit will be applied to their wallet.
   - **Heavy Freight:** Check line items. If `weight_kg` > 5.0, `suggested_action` MUST be 'SCHEDULE_FREIGHT_PICKUP'. You must draft a reply asking when a truck can pick it up, do NOT tell them to drop it at Aramex.
   - **Return Fraud:** Look at the `Customer VIP Profile`. If `total_returns_count` > 3, this is serial returning. Set `requires_human_escalation` = True, state "Fraud Review required" as the reason.
   - **Wallets:** If `wallet_balance_aed` > 0, proactively suggest they might want their refund quickly sent to their existing Mumzworld wallet.
   - **Active Double Dipping:** If `active_return_in_progress` is True, politely tell them "Your return is already being processed, please wait" and set `suggested_action` = 'NONE'.
   - **Warranties:** If they want to return something > 14 days old, but it has `warranty` > 0 in the catalogue, DO NOT reject them. Change intent to `WARRANTY_CLAIM` and instruct them to contact the manufacturer.
   - **International Customs:** Check `shipping_address`. If the `country` is NOT "UAE" (e.g. "KSA"), you must warn them that a 50 AED cross-border customs fee will be deducted for their return.
   - **Out of Stock Exchanges:** If they specify they want an EXCHANGE, but the item's `in_stock` value is False (found in the `line_items` array), you MUST pivot gracefully. Under NO CIRCUMSTANCES should the intent be EXCHANGE. You MUST set intent to `STORE_CREDIT` or `REFUND` instead, and apologize that an exchange is impossible due to stock shortages.
   
4. **DEEP NUANCE COMPREHENSION (ALL CUSTOMER SCENARIOS)**
   - Delays: If the order `status` is "PENDING" or "SHIPPED" but `delivery_date` is None or running late, respond with heavy empathy and apologize for logistics delays.
   - Mixed signals: Look out for "Anything the customer can say". Be incredibly intelligent. Do not hallucinate, but always apply heavy situational awareness. If confused, ask clarifying questions instead of making blind actions.

4. **MULTIMODAL VERIFICATION**
   - If claiming defect, check the visual feed! If an image is provided in your context, you MUST deeply engage with it. If they claim a stroller is broken, look at the uploaded image. If it shows severe damage, grant the exception or escalate to management as needed. If the image shows unhygienic states, reject it.
   - If they mention a defect but NO image is provided, your `suggested_action` can be NONE and you MUST draft a reply asking them to upload a photo for verification.

5. **VIP EXCEPTIONS**
   - If `vip_status` is true, authorize bending standard 7-day return limits up to 14 days.

6. **LANGUAGE RULES (BILINGUAL OBLIGATION)**
   - `draft_reply_en`: Empathetic, professional, clear English.
   - `draft_reply_ar`: Expert, colloquial, polite Arabic transcreation (Fusha). Pure native tone.

You must output exactly according to the requested JSON schema, particularly ensuring `suggested_action` rigidly targets ONE of the exact enum string options defined in the schema.
"""
    
    from langchain_core.messages import HumanMessage
    
    content_blocks = [{"type": "text", "text": system_prompt}]
    
    if state.get("image_base64"):
        content_blocks.append({
            "type": "image_url", 
            "image_url": {"url": state["image_base64"]}
        })
        
    payload = [HumanMessage(content=content_blocks)]

    # 3-Tier High Availability Cascade
    try:
        print("[NODE] Executing [PRIMARY] Google Gemini...")
        result = structured_gemini.invoke(payload)
    except Exception as e_gemini:
        print(f"[NODE] PRIMARY FAILED ({e_gemini}). Cascading to [SECONDARY] OpenRouter...")
        try:
            result = structured_openrouter.invoke(payload)
        except Exception as e_openrouter:
            print(f"[NODE] SECONDARY FAILED ({e_openrouter}). Cascading to [TERTIARY] Z.AI Text-Only...")
            
            # GLM-4.7-Flash is a Text-Only model. 
            # We MUST strip the Multimodal Base64 Image array to prevent a fatal 400 crash on Z.AI.
            text_only_blocks = [{"type": "text", "text": system_prompt}]
            result = structured_zai.invoke([HumanMessage(content=text_only_blocks)])

    state["final_response"] = result
    return state


# ---------------------------------------------------------
# COMPILE THE GRAPH
# ---------------------------------------------------------
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("extract_intent", node_extract_intent)
workflow.add_node("tool_db_lookup", node_tool_db_lookup)
workflow.add_node("rag_policy_lookup", node_rag_policy_lookup)
workflow.add_node("synthesize_response", node_synthesize_response)

# Define Edges (The linear flow, though LangGraph allows loops)
workflow.add_edge(START, "extract_intent")
workflow.add_edge("extract_intent", "tool_db_lookup")
workflow.add_edge("tool_db_lookup", "rag_policy_lookup")
workflow.add_edge("rag_policy_lookup", "synthesize_response")
workflow.add_edge("synthesize_response", END)

# Compile the agent
triage_agent = workflow.compile()
