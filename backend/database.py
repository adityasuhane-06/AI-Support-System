import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['mumzworld_triage_db']
orders_coll = db['orders']
customers_coll = db['customers']

def get_order_details(order_id: str) -> dict:
    """Fetch order details from MongoDB."""
    order = orders_coll.find_one({"order_id": order_id}, {"_id": 0})
    return order if order else None

def get_customer_details(customer_id: str) -> dict:
    """Fetch customer VIP status and LTV."""
    customer = customers_coll.find_one({"customer_id": customer_id}, {"_id": 0})
    return customer if customer else None
