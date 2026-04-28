import random
from pymongo import MongoClient
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('en_US')  # Fallback to standard US locale to avoid library misses

MONGO_URI = "mongodb+srv://adityasuhanecsds22_db_user:rhURxnBj6DRri8xi@cluster0.xjmpt7f.mongodb.net/?appName=Cluster0"

# Real Mumzworld Catalog Categories (With Analytics/Logistics Metadata)
MUMZWORLD_CATALOG = [
    {"product_id": "P-D01", "name": "Pampers Premium Care Diapers Size 3", "brand": "Pampers", "category": "Diapering & Hygiene", "is_returnable": False, "price_aed": 115.00, "warranty": 0, "weight_kg": 2.5, "image_url": "https://m.media-amazon.com/images/I/71Y86x1rJvL._AC_SX679_.jpg", "in_stock": True},
    {"product_id": "P-D02", "name": "WaterWipes Baby Wipes - 60 Wipes (12 Packs)", "brand": "WaterWipes", "category": "Diapering & Hygiene", "is_returnable": False, "price_aed": 199.00, "warranty": 0, "weight_kg": 4.0, "image_url": "https://m.media-amazon.com/images/I/71fL9W7A7pL._AC_SX679_.jpg", "in_stock": True},
    {"product_id": "P-G01", "name": "Bugaboo Fox 5 Stroller - Midnight Black", "brand": "Bugaboo", "category": "Travel & Gear", "is_returnable": True, "price_aed": 4500.00, "warranty": 24, "weight_kg": 12.2, "image_url": "https://images.unsplash.com/photo-1540479859555-17af45c78602?auto=format&fit=crop&w=500", "in_stock": False}, # OUT OF STOCK
    {"product_id": "P-G02", "name": "Doona Infant Car Seat & Latch Base", "brand": "Doona", "category": "Travel & Gear", "is_returnable": True, "price_aed": 2200.00, "warranty": 24, "weight_kg": 7.5, "image_url": "https://images.unsplash.com/photo-1510531704581-5b287097205d?auto=format&fit=crop&w=500", "in_stock": True},
    {"product_id": "P-F01", "name": "Medela Swing Maxi Flex Double Electric Breast Pump", "brand": "Medela", "category": "Feeding & Hygiene", "is_returnable": False, "price_aed": 1250.00, "warranty": 12, "weight_kg": 1.2, "image_url": "https://m.media-amazon.com/images/I/61rU8j8lVYL._AC_SX679_.jpg", "in_stock": True},
    {"product_id": "P-F02", "name": "Aptamil Advance 1 Infant Formula Milk (800g)", "brand": "Aptamil", "category": "Feeding", "is_returnable": False, "price_aed": 85.00, "warranty": 0, "weight_kg": 0.8, "image_url": "https://m.media-amazon.com/images/I/71rIe7oW6TL._AC_SX679_.jpg", "in_stock": True},
    {"product_id": "P-F03", "name": "Tommee Tippee Closer to Nature Bottles (Pack of 3)", "brand": "Tommee Tippee", "category": "Feeding", "is_returnable": False, "price_aed": 110.00, "warranty": 0, "weight_kg": 0.3, "image_url": "https://m.media-amazon.com/images/I/71T1XWJt8SL._AC_SX679_.jpg", "in_stock": True},
    {"product_id": "P-N01", "name": "Nanit Pro Smart Baby Monitor & Floor Stand", "brand": "Nanit", "category": "Nursery & Safety", "is_returnable": True, "price_aed": 1450.00, "warranty": 12, "weight_kg": 5.0, "image_url": "https://m.media-amazon.com/images/I/61vK6H2p-xL._AC_SX679_.jpg", "in_stock": True},
    {"product_id": "P-N02", "name": "Stokke Tripp Trapp High Chair - Natural", "brand": "Stokke", "category": "Nursery", "is_returnable": True, "price_aed": 990.00, "warranty": 84, "weight_kg": 7.0, "image_url": "https://m.media-amazon.com/images/I/71Xm+P4zJAL._AC_SX679_.jpg", "in_stock": True},
    {"product_id": "P-M01", "name": "Frida Mom Postpartum Recovery Essentials Kit", "brand": "Frida Mom", "category": "Maternity", "is_returnable": False, "price_aed": 240.00, "warranty": 0, "weight_kg": 2.0, "image_url": "https://m.media-amazon.com/images/I/81IIfx3bZkL._AC_SX679_.jpg", "in_stock": True}
]

def format_address():
    locations = [{"city": "Dubai", "country": "UAE"}, {"city": "Abu Dhabi", "country": "UAE"}, {"city": "Riyadh", "country": "KSA"}, {"city": "Jeddah", "country": "KSA"}]
    loc = random.choice(locations)
    return {
        "street": fake.street_address(),
        "area": fake.city_suffix(),
        "city": loc["city"],
        "country": loc["country"]
    }

def seed_comprehensive_database():
    print("Initiating connection to MongoDB (Mumzworld Data Warehouse Simulation)...")
    client = MongoClient(MONGO_URI)
    db = client['mumzworld_triage_db']
    
    orders_coll = db['orders']
    customers_coll = db['customers']
    
    print("Flushing existing records...")
    orders_coll.delete_many({})
    customers_coll.delete_many({})
    
    now = datetime.utcnow()
    
    customers = []
    orders = []

    # 1. HARDCODED EVALUATION DATA (Required for Pytest assertions)
    eval_customers = [
        {"customer_id": "CUST-001", "name": "Sarah Miller", "email": "sarah.miller@example.com", "phone": "+971501234567", "account_created_at": (now - timedelta(days=800)).isoformat(), "vip_status": True, "loyalty_tier": "Platinum", "lifetime_value_aed": 14500.50, "total_orders_count": 42, "total_returns_count": 1, "wallet_balance_aed": 500.00},
        {"customer_id": "CUST-002", "name": "Fatima Al Fasi", "email": "fatima.alfasi@example.com", "phone": "+971559876543", "account_created_at": (now - timedelta(days=45)).isoformat(), "vip_status": False, "loyalty_tier": "Silver", "lifetime_value_aed": 300.00, "total_orders_count": 1, "total_returns_count": 0, "wallet_balance_aed": 0.00},
        {"customer_id": "CUST-003", "name": "Aisha Khan", "email": "aisha.khan99@example.com", "phone": "+971523456789", "account_created_at": (now - timedelta(days=200)).isoformat(), "vip_status": False, "loyalty_tier": "Gold", "lifetime_value_aed": 1200.00, "total_orders_count": 5, "total_returns_count": 4, "wallet_balance_aed": 100.00} # High return rate!
    ]
    customers.extend(eval_customers)

    eval_orders = [
        # Standard Order but Gifted!
        {"order_id": "MW-12345", "customer_id": "CUST-001", "order_date": (now - timedelta(days=12)).isoformat(), "delivery_date": (now - timedelta(days=10)).isoformat(), "status": "DELIVERED", "payment_method": "APPLE_PAY", "payment_status": "PAID", "is_gift": True, "active_return_in_progress": False, "promo_code_used": None, "shipping_address": {"street": "Villa 14", "area": "Jumeirah 3", "city": "Dubai", "country": "UAE"}, "tracking_number": "ARAMEX-99887766", "carrier": "Aramex", "return_eligible_until": (now - timedelta(days=3)).isoformat(), "total_aed": 4585.00, "line_items": [MUMZWORLD_CATALOG[2], MUMZWORLD_CATALOG[0]]},
        # Hygiene Trap (Active Return Already Progressing)
        {"order_id": "MW-12346", "customer_id": "CUST-002", "order_date": (now - timedelta(days=5)).isoformat(), "delivery_date": (now - timedelta(days=2)).isoformat(), "status": "DELIVERED", "payment_method": "CREDIT_CARD", "payment_status": "PAID", "is_gift": False, "active_return_in_progress": True, "promo_code_used": "WELCOME20", "shipping_address": {"street": "Apt 205", "area": "Marina", "city": "Dubai", "country": "UAE"}, "tracking_number": "FETCH-11223344", "carrier": "Fetchr", "return_eligible_until": (now + timedelta(days=5)).isoformat(), "total_aed": 1250.00, "line_items": [MUMZWORLD_CATALOG[4]]},
        # Lost in Transit Trap / Fraud Tester
        {"order_id": "MW-12347", "customer_id": "CUST-003", "order_date": (now - timedelta(days=10)).isoformat(), "delivery_date": None, "status": "SHIPPED", "payment_method": "COD", "payment_status": "PENDING_COD", "is_gift": False, "active_return_in_progress": False, "promo_code_used": None, "shipping_address": {"street": "House 45", "area": "Khalifa City", "city": "Abu Dhabi", "country": "UAE"}, "tracking_number": "QN-554433", "carrier": "Quiqup", "return_eligible_until": None, "total_aed": 990.00, "line_items": [MUMZWORLD_CATALOG[8]]},
        
        # PHASE 3 EDGE-CASE SPECIFIC EVAL ORDERS:
        
        # WARRANTY CLAIM (>14 days, has electronics 12 month warranty)
        {"order_id": "MW-80001", "customer_id": "CUST-002", "order_date": (now - timedelta(days=200)).isoformat(), "delivery_date": (now - timedelta(days=195)).isoformat(), "status": "DELIVERED", "is_gift": False, "active_return_in_progress": False, "shipping_address": {"country": "UAE"}, "return_eligible_until": (now - timedelta(days=188)).isoformat(), "total_aed": 1450.00, "line_items": [MUMZWORLD_CATALOG[7]]},
        # KSA INTERNATIONAL FEE Order (Using a Returnable Item: Car Seat)
        {"order_id": "MW-80002", "customer_id": "CUST-001", "order_date": (now - timedelta(days=3)).isoformat(), "delivery_date": (now - timedelta(days=1)).isoformat(), "status": "DELIVERED", "is_gift": False, "active_return_in_progress": False, "shipping_address": {"country": "KSA"}, "return_eligible_until": (now + timedelta(days=6)).isoformat(), "total_aed": 2200.00, "line_items": [MUMZWORLD_CATALOG[3]]},
        # OUT OF STOCK Bugaboo Exchange Attempt
        {"order_id": "MW-80003", "customer_id": "CUST-003", "order_date": (now - timedelta(days=4)).isoformat(), "delivery_date": (now - timedelta(days=2)).isoformat(), "status": "DELIVERED", "is_gift": False, "active_return_in_progress": False, "shipping_address": {"country": "UAE"}, "return_eligible_until": (now + timedelta(days=5)).isoformat(), "total_aed": 4500.00, "line_items": [MUMZWORLD_CATALOG[2]]}
    ]
    orders.extend(eval_orders)

    # 2. BULK GENERATION FOR "MUMZWORLD EXACT DATA" (~50 Customers, ~150 Orders)
    print("Generating bulk customer and catalog combinations...")
    bulk_customer_ids = []
    for _ in range(50):
        c_id = f"CUST-{fake.random_int(1000, 9999)}"
        bulk_customer_ids.append(c_id)
        is_vip = fake.boolean(chance_of_getting_true=15)
        tc_count = fake.random_int(1, 100)
        ret_count = fake.random_int(0, tc_count) # Return counts bounded by total orders.
        customers.append({
            "customer_id": c_id,
            "name": fake.name(),
            "email": fake.email(),
            "phone": "+971" + str(fake.random_int(500000000, 599999999)),
            "account_created_at": (now - timedelta(days=fake.random_int(10, 1000))).isoformat(),
            "vip_status": is_vip,
            "loyalty_tier": "Platinum" if is_vip else random.choice(["Silver", "Gold"]),
            "lifetime_value_aed": round(random.uniform(100, 25000), 2),
            "total_orders_count": tc_count,
            "total_returns_count": ret_count,
            "wallet_balance_aed": round(random.uniform(0, 1500), 2) if fake.boolean(20) else 0.00
        })

    for _ in range(150):
        c_id = random.choice(bulk_customer_ids)
        delivery_status = random.choice(["PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "RETURNED", "CANCELED"])
        o_date = now - timedelta(days=fake.random_int(1, 30))
        d_date = (o_date + timedelta(days=random.randint(1, 4))) if delivery_status in ["DELIVERED", "RETURNED"] else None

        cart_items = random.sample(MUMZWORLD_CATALOG, k=random.randint(1, 4))
        cart_total = sum(i["price_aed"] for i in cart_items)

        orders.append({
            "order_id": f"MW-{fake.random_int(20000, 99999)}",
            "customer_id": c_id,
            "order_date": o_date.isoformat(),
            "delivery_date": d_date.isoformat() if d_date else None,
            "status": delivery_status,
            "payment_method": random.choice(["CREDIT_CARD", "APPLE_PAY", "MUMZWORLD_WALLET", "COD"]),
            "payment_status": "PAID" if delivery_status != "CANCELED" else "REFUNDED",
            "is_gift": fake.boolean(chance_of_getting_true=20),
            "active_return_in_progress": fake.boolean(chance_of_getting_true=5) if delivery_status == "DELIVERED" else False,
            "promo_code_used": random.choice([None, "WELCOME10", "MUM15", "FREESHIP"]),
            "shipping_address": format_address(),
            "tracking_number": f"{random.choice(['ARAMEX', 'FETCHR', 'QUIQUP'])}-{fake.random_int(1000000, 9999999)}",
            "carrier": random.choice(['Aramex', 'Fetchr', 'Quiqup']),
            "return_eligible_until": (d_date + timedelta(days=7)).isoformat() if d_date else None,
            "total_aed": cart_total,
            "line_items": cart_items
        })
    
    # 3. DB COMMIT
    print(f"Writing {len(customers)} unique users and {len(orders)} catalog combinations to MongoDB Cluster...")
    customers_coll.insert_many(customers)
    orders_coll.insert_many(orders)
    
    print("DATABASE SEED COMPLETION VERIFIED. Noise and dataset width highly enriched.")

if __name__ == "__main__":
    seed_comprehensive_database()
