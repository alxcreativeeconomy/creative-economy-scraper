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
# PHASE 2: GLOBAL-TO-AFRICA SCOUTING
# ============================================================================
def aggressive_autonomous_sweep():
    print("--> [INTEL] Initiating Global Inbound Capital Sweep (US/EU -> Africa)...")
    
    # Using your API key
    api_key = "AIzaSyDXYq9YL99fGB7sTuMjgKygk4XO0zmjWC8" 
    
    # Switched to the more stable 'gemini-2.5-flash' model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    source_markets = "United States, European Union, United Kingdom"
    target_regions = "Pan-African, South Africa, Ghana, Egypt, Rwanda, Cameroon, Ethiopia, Nigeria, Morocco"
    categories = "Production, Capacity building, Training, Upskilling, Investment, Eco-System Partners, AI related initiatives for the creative sector"
    
    prompt = f"""
    You are the Head of Business Development for ALX Africa. 
    TASK: Perform a deep reconnaissance sweep of the web for live 2026 funding, tenders, and RFPs.
    
    CRITICAL MANDATE: You must search for deals ORIGINATING in the {source_markets} that are explicitly earmarked for investment, aid, or partnership in {target_regions}.
    
    CATEGORIES: {categories}
    
    Look specifically for: 
    - USAID, USADF, or DFC (US International Development Finance Corp) digital tech grants for Africa.
    - Horizon Europe or European Commission tenders for African digital upskilling.
    - UK FCDO (Foreign, Commonwealth & Development Office) creative economy funds.
    
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
        response = None
        error_message = ""
        
        for delay in [1, 2, 4]:
            res = requests.post(url, json=payload, timeout=45)
            if res.status_code == 200:
                response = res
                break
            else:
                # Capture the EXACT error Google is throwing
                error_message = res.text
            time.sleep(delay)
        
        if not response:
            print(f"[X] Scout Network unavailable. Google API Error: {error_message}")
            return

        results = response.json()
        
        try:
            text_content = results['candidates'][0]['content']['parts'][0]['text']
            # Clean up JSON just in case Gemini adds markdown backticks
            clean_json = text_content.replace('```json', '').replace('```', '').strip()
            deals = json.loads(clean_json)
        except Exception as parse_err:
            print(f"[X] Failed to parse AI response into JSON: {parse_err}")
            print(f"Raw Output: {results}")
            return
        
        if isinstance(deals, list):
            print(f"    [+] Scout found {len(deals)} Global-to-Africa Institutional Leads.")
            for deal in deals:
                deal['tags'] = ["Foreign Capital", "AI Discovered", deal.get('country', 'Pan-African')]
                save_to_database(deal)
                
    except Exception as e:
        print(f"    [X] Strategic sweep failed entirely: {e}")

# ============================================================================
# PHASE 3: UPSERT LOGIC
# ============================================================================
def save_to_database(deal_data):
    if db is None: return
    try:
        docs = db.collection('opportunities').where('title', '==', deal_data.get('title', '')).limit(1).get()
        
        if docs:
            doc_id = docs[0].id
            db.collection('opportunities').document(doc_id).update(deal_data)
            print(f"    [~] UPDATED Strategy: {deal_data.get('title')}")
        else:
            db.collection('opportunities').add(deal_data)
            print(f"    [+] SECURED NEW GLOBAL LEAD: {deal_data.get('title')}")
            
    except Exception as e:
        print(f"    [X] Database Sync Error: {e}")

def run_harvester():
    print("\n" + "="*60)
    print("🚀 ALX GLOBAL INTELLIGENCE HARVESTER (US/EU -> AFRICA): ONLINE")
    print("="*60 + "\n")
    
    aggressive_autonomous_sweep()
    
    print("\n" + "="*60)
    print("✅ HARVESTER CYCLE COMPLETE. STRATEGIC MATRIX SYNCED.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_harvester()