import os
import time
import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# ============================================================================
# PHASE 1: DATABASE INITIALIZATION
# ============================================================================
try:
    if not firebase_admin._apps:
        key_path = os.getenv('FIREBASE_KEY_PATH', 'firebase-key.json')
        if os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("[+] Firebase Business Intelligence Link established.")
        else:
            db = None
            print("[!] Warning: Missing security key. Simulation mode.")
except Exception as e:
    db = None
    print(f"[X] Init Error: {e}")

# ============================================================================
# PHASE 2: AGGRESSIVE SCOUTING (BUSINESS HEAD LOGIC)
# ============================================================================
def aggressive_autonomous_sweep():
    """
    Acts as a Business Head. Searches specifically for Mega-Funds, PPPs,
    and Institutional Tenders for 2026 across target African markets.
    """
    print("--> [INTEL] Initiating Aggressive Strategic Sweep...")
    
    api_key = "" # System provides key at runtime
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
    
    # Priority Regions & Sectors from Business Head Mandate
    regions = "South Africa, Ghana, Egypt, Rwanda, Cameroon, Ethiopia, Nigeria, Morocco"
    categories = "Production, Capacity building, Training, Upskilling, Investment, Eco-System Partners, AI for Creative Sector"
    
    prompt = f"""
    You are the Head of Business Development for ALX Africa. 
    TASK: Perform a high-level reconnaissance sweep of the web for live 2026 funding, tenders, and RFPs.
    
    TARGETS: {regions}
    FOCUS: {categories}
    
    CRITERIA FOR 'ALX FIT':
    1. Scale: Can this deal train 10,000+ youth?
    2. Infrastructure: Can we host this at an ALX Physical Hub?
    3. Technical: Does it require SWE, AI, or Cloud Computing expertise?
    
    Look for: AfDB 'i-DICE' tenders, Mastercard Foundation RFPs, World Bank Creative Tech grants, 
    AUDA-NEPAD SIFA projects, and Ministry of Tech Tenders in Morocco and Egypt.
    
    Format: JSON Array of Objects with:
    title, source, country, value (be specific about millions), deadline, 
    strategicFit (Why ALX wins this), businessAction (Next steps for our team), 
    status (Open/Urgent), sector, category, eligibility, portalUrl, matchScore (90-99).
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": { "responseMimeType": "application/json" }
    }

    try:
        # Exponential backoff for API reliability
        response = None
        for delay in [1, 2, 4]:
            res = requests.post(url, json=payload, timeout=40)
            if res.status_code == 200:
                response = res
                break
            time.sleep(delay)
        
        if not response:
            print("[X] Scout Network unavailable.")
            return

        results = response.json()
        deals = json.loads(results['candidates'][0]['content']['parts'][0]['text'])
        
        if isinstance(deals, list):
            print(f"    [+] Scout found {len(deals)} Strategic Institutional Leads.")
            for deal in deals:
                # Add ALX business logic tags
                deal['tags'] = ["AI Discovered", deal.get('country', 'Pan-African'), "Mega-Fund"]
                save_to_database(deal)
    except Exception as e:
        print(f"    [X] Strategic sweep failed: {e}")

# ============================================================================
# PHASE 3: UPSERT LOGIC (PREVENT DUPLICATES)
# ============================================================================
def save_to_database(deal_data):
    if db is None: return
    try:
        # Business ID: Unique title-source combo
        # Checking title to update status if deal already exists
        docs = db.collection('opportunities').where('title', '==', deal_data['title']).limit(1).get()
        
        if docs:
            doc_id = docs[0].id
            db.collection('opportunities').document(doc_id).update(deal_data)
            print(f"    [~] UPDATED Strategy: {deal_data['title']}")
        else:
            db.collection('opportunities').add(deal_data)
            print(f"    [+] SECURED NEW LEAD: {deal_data['title']}")
            
    except Exception as e:
        print(f"    [X] Database Sync Error: {e}")

def run_harvester():
    print("\n" + "="*60)
    print("🚀 ALX CREATIVE ECONOMY INTELLIGENCE HARVESTER: ONLINE")
    print("="*60 + "\n")
    
    aggressive_autonomous_sweep()
    
    print("\n" + "="*60)
    print("✅ HARVESTER CYCLE COMPLETE. STRATEGIC MATRIX SYNCED.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_harvester()