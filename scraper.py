import os
import time
import json
import random
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# ============================================================================
# PHASE 1: SYSTEM INITIALIZATION
# ============================================================================
try:
    if not firebase_admin._apps:
        # Use environment variable or local file
        key_path = os.getenv('FIREBASE_KEY_PATH', 'firebase-key.json')
        if os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("[+] Firebase connection established.")
        else:
            db = None
            print("[!] Warning: No Firebase key. Simulation mode.")
except Exception as e:
    db = None
    print(f"[X] Initialization Error: {e}")

# ============================================================================
# PHASE 2: THE AUTONOMOUS SCOUT (GEMINI API)
# ============================================================================
def autonomous_deep_sweep():
    """
    Uses Gemini 2.5 Flash + Google Search to discover real-world 
    Creative Economy deals without hardcoded URLs.
    """
    print("--> [AI] Initiating Autonomous Deep Sweep...")
    
    api_key = "" # Execution environment provides the key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
    
    regions = "South Africa, Ghana, Egypt, Rwanda, Cameroon, Ethiopia, Nigeria, Morocco"
    categories = "Production, Capacity building, Training, Upskilling, Investment, Eco-System Partners, AI related initiatives"
    
    prompt = f"""
    Search the live web for the latest high-value creative economy funding, RFPs, and tenders for 2026.
    TARGET REGIONS: {regions}
    TARGET CATEGORIES: {categories}
    
    Think like a Business Head at ALX Africa. We are looking for deals that allow us to use our 
    existing hubs and tech talent (Software Engineers, AI specialists).
    
    Return the results as a JSON array of objects with exactly these fields:
    title, source, country, type, status (Open/Forecast), sector, category (Business Only/B2B Partnership), 
    value (in USD/Euro), deadline, description, eligibility, strategicFit (Why it fits ALX specifically), portalUrl.
    
    Assign a 'matchScore' from 1-100 based on how well it fits ALX.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    try:
        # Exponential backoff implementation
        for attempt in [1, 2, 4, 8, 16]:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                break
            time.sleep(attempt)
        
        results = response.json()
        text_content = results['candidates'][0]['content']['parts'][0]['text']
        deals = json.loads(text_content)
        
        if isinstance(deals, list):
            print(f"    [+] AI discovered {len(deals)} autonomous leads.")
            for deal in deals:
                save_to_database(deal)
        return True
    except Exception as e:
        print(f"    [X] Autonomous search failed: {e}")
        return False

# ============================================================================
# PHASE 3: SMART PERSISTENCE (UPSERTS)
# ============================================================================
def save_to_database(deal_data):
    if db is None: return
    
    try:
        # Standardize for ALX Business Intelligence
        deal_data['tags'] = deal_data.get('tags', []) + ["AI Discovered", deal_data.get('country', 'Global')]
        deal_data['lastScanned'] = firestore.SERVER_TIMESTAMP
        
        # Check for duplicates by title
        docs = db.collection('opportunities').where('title', '==', deal_data['title']).limit(1).get()
        
        if docs:
            # Update existing
            doc_id = docs[0].id
            db.collection('opportunities').document(doc_id).update(deal_data)
            print(f"    [~] Updated: {deal_data['title']}")
        else:
            # Add new
            db.collection('opportunities').add(deal_data)
            print(f"    [+] New High-Value Lead: {deal_data['title']}")
            
    except Exception as e:
        print(f"    [X] DB Error: {e}")

def run_harvester():
    print("\n" + "="*55)
    print("🚀 ALX CREATIVE ECONOMY AUTONOMOUS ENGINE INITIATED")
    print("="*55 + "\n")
    
    # Run the autonomous intelligence sweep
    success = autonomous_deep_sweep()
    
    if success:
        print("\n" + "="*55)
        print("✅ SWEEP COMPLETE. DATABASE SYNCED.")
        print("="*55 + "\n")
    else:
        print("\n[!] Sweep encountered issues. Check API status.\n")

if __name__ == "__main__":
    run_harvester()