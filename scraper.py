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
        # Render looks for the key at this path
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
# PHASE 2: GLOBAL-TO-AFRICA SCOUTING (BUSINESS HEAD LOGIC)
# ============================================================================
def aggressive_autonomous_sweep():
    """
    Acts as a Business Head. Searches specifically for US and EU Mega-Funds, 
    USAID/EC Grants, and FDI earmarked for the African Creative & Tech economies.
    """
    print("--> [INTEL] Initiating Global Inbound Capital Sweep (US/EU -> Africa)...")
    
    api_key = "AIzaSyDXYq9YL99fGB7sTuMjgKygk4XO0zmjWC8" # System provides key at runtime
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
    
    # Global to Local Strategy
    source_markets = "United States, European Union, United Kingdom"
    target_regions = "Pan-African, South Africa, Ghana, Egypt, Rwanda, Cameroon, Ethiopia, Nigeria, Morocco"
    categories = "Production, Capacity building, Training, Upskilling, Investment, Eco-System Partners, AI related initiatives for the creative sector"
    
    prompt = f"""
    You are the Head of Business Development for ALX Africa. 
    TASK: Perform a deep reconnaissance sweep of the web for live 2026 funding, tenders, and RFPs.
    
    CRITICAL MANDATE: You must search for deals ORIGINATING in the {source_markets} that are explicitly earmarked for investment, aid, or partnership in {target_regions}.
    
    CATEGORIES: {categories}
    
    CRITERIA FOR 'ALX FIT':
    1. Scale: Can this US/EU capital train 10,000+ African youth or handle multi-million dollar budgets?
    2. Infrastructure: Can we act as the 'boots-on-the-ground' African execution partner using ALX Physical Hubs?
    3. Technical: Does it involve AI, Software Engineering, or Cloud Computing?
    
    Look specifically for: 
    - USAID, USADF, or DFC (US International Development Finance Corp) digital tech grants for Africa.
    - Horizon Europe or European Commission tenders for African digital upskilling.
    - UK FCDO (Foreign, Commonwealth & Development Office) creative economy funds.
    - US/EU-based private foundations (e.g., Ford, Gates, Skoll) Mega-Funds targeting African youth.
    
    Format the response as a JSON Array of Objects with these fields:
    title, source (The US/EU organization), country (The African target country), value (be specific about millions if possible), deadline, 
    strategicFit (Explain why ALX is the perfect local execution partner for this foreign capital), 
    businessAction (Step-by-step next steps for our partnerships team to bid), 
    status (Open/Urgent/Forecast), sector, category, eligibility, portalUrl, matchScore (90-99).
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
            res = requests.post(url, json=payload, timeout=45)
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
            print(f"    [+] Scout found {len(deals)} Global-to-Africa Institutional Leads.")
            for deal in deals:
                # Add ALX business logic tags identifying foreign capital
                deal['tags'] = ["Foreign Capital", "AI Discovered", deal.get('country', 'Pan-African')]
                save_to_database(deal)
    except Exception as e:
        print(f"    [X] Strategic sweep failed: {e}")

# ============================================================================
# PHASE 3: UPSERT LOGIC (PREVENT DUPLICATES)
# ============================================================================
def save_to_database(deal_data):
    if db is None: return
    try:
        # Standardize matching by title
        docs = db.collection('opportunities').where('title', '==', deal_data['title']).limit(1).get()
        
        if docs:
            doc_id = docs[0].id
            db.collection('opportunities').document(doc_id).update(deal_data)
            print(f"    [~] UPDATED Strategy: {deal_data['title']}")
        else:
            db.collection('opportunities').add(deal_data)
            print(f"    [+] SECURED NEW GLOBAL LEAD: {deal_data['title']}")
            
    except Exception as e:
        print(f"    [X] Database Sync Error: {e}")

def run_harvester():
    print("\n" + "="*60)
    print("🚀 ALX GLOBAL INTELLIGENCE HARVESTER (US/EU -> AFRICA): ONLINE")
    print("="*60 + "\n")
    
    # Perform the deep global autonomous sweep
    aggressive_autonomous_sweep()
    
    print("\n" + "="*60)
    print("✅ HARVESTER CYCLE COMPLETE. STRATEGIC MATRIX SYNCED.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_harvester()