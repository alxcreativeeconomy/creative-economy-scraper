import requests
from bs4 import BeautifulSoup
import time
import os
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# ============================================================================
# PHASE 1: FIREBASE INITIALIZATION
# ============================================================================
try:
    if not firebase_admin._apps:
        key_path = os.getenv('FIREBASE_KEY_PATH', 'firebase-key.json')
        if os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("[+] Firebase connection established successfully.")
        else:
            db = None
            print(f"[!] Warning: {key_path} not found. Running in simulation mode.")
except Exception as e:
    db = None
    print(f"[X] Firebase initialization error: {e}")


# ============================================================================
# PHASE 2: SMART DATABASE SAVING (UPSERTS)
# ============================================================================
def save_to_database(deal_data):
    """
    Checks if a deal already exists. If it does, it updates the status (Open/Closed).
    If it's new, it adds it to the database. This prevents duplicates!
    """
    if db is not None:
        try:
            # Fetch all documents to check for existing titles (Firebase safe query)
            existing_docs = db.collection('opportunities').stream()
            doc_id_to_update = None
            
            for doc in existing_docs:
                if doc.to_dict().get('title') == deal_data['title']:
                    doc_id_to_update = doc.id
                    break
            
            if doc_id_to_update:
                # Update the existing past/closed deal with new status
                db.collection('opportunities').document(doc_id_to_update).set(deal_data, merge=True)
                print(f"    [~] UPDATED Past/Existing Deal: {deal_data['title']} -> Status: {deal_data['status']}")
            else:
                # Add entirely new deal
                deal_data['tags'] = deal_data.get('tags', []) + ["Engine Discovered"]
                if 'matchScore' not in deal_data:
                    deal_data['matchScore'] = random.randint(70, 95)
                    
                db.collection('opportunities').add(deal_data)
                print(f"    [+] NEW DEAL Pushed to Firebase: {deal_data['title']}")
        except Exception as e:
            print(f"    [X] Failed to interact with Firebase: {e}")
    else:
        print(f"    [SIM] Found Deal: {deal_data['title']} - Status: {deal_data['status']}")


def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        return None
    except:
        return None


# ============================================================================
# PHASE 3: HISTORICAL / MOCK DATA INJECTOR
# ============================================================================
def inject_historical_mock_data():
    """
    Seeds the database with all past, closed, and strategic deals you had in React.
    """
    historical_deals = [
        { "title": "Epic MegaGrants for 3D & Animation", "source": "Epic Games", "country": "Pan-African", "type": "Tech Grant / Partnership", "status": "Open", "sector": "Tech & Innovation", "category": "B2B Partnership", "value": "$5,000 - $500,000", "deadline": "Rolling", "description": "Real-world grant by Epic Games supporting creators using Unreal Engine.", "eligibility": "Studios using Unreal Engine.", "strategicFit": "ALX SWEET SPOT. Connect ALX software engineers directly to Epic.", "portalUrl": "https://www.unrealengine.com/", "businessAction": ["Establish an ALX Unreal Engine training track."], "matchScore": 99 },
        { "title": "MultiChoice Talent Factory (MTF) Academy", "source": "MultiChoice Group", "country": "Nigeria, Kenya, South Africa", "type": "Capacity Building", "status": "Forecast", "sector": "Film & TV", "category": "B2B Partnership", "value": "Full Scholarship", "deadline": "Est. Jun 2026", "description": "Africa's premier film training program seeking tech partners.", "eligibility": "Emerging filmmakers, tech integrators.", "strategicFit": "Partner with MTF to supply Cloud curriculum.", "portalUrl": "https://multichoicetalentfactory.com/", "businessAction": ["Initiate B2B discussions with MTF."], "matchScore": 95 },
        { "title": "Fak'ugesi Digital Innovation Residency", "source": "Fak'ugesi Festival", "country": "South Africa", "type": "Ecosystem Partnership", "status": "Closed", "sector": "Tech & Innovation", "category": "B2B Partnership", "value": "Residency & Grant", "deadline": "Past", "description": "Residency for digital artists and creative technologists.", "eligibility": "Digital creatives.", "strategicFit": "Sponsor a Generative AI hackathon here.", "portalUrl": "https://fakugesi.co.za/", "businessAction": ["Pitch Fak'ugesi organizers."], "matchScore": 92 },
        { "title": "Afreximbank CANEX Deal Room", "source": "CANEX", "country": "Pan-African", "type": "Investment", "status": "Open", "sector": "Finance", "category": "B2B Partnership", "value": "$250,000+ Debt/Equity", "deadline": "Rolling", "description": "Bankable finance for creative businesses to export.", "eligibility": "Registered businesses with 3+ years financials.", "strategicFit": "Scaling vehicle for ALX startups.", "portalUrl": "https://canex.africa/", "businessAction": ["Create ALX to CANEX readiness program."], "matchScore": 96 },
        { "title": "MEST Africa Challenge", "source": "MEST", "country": "Ghana/Pan-African", "type": "Incubator", "status": "Closed", "sector": "Tech & Innovation", "category": "B2B Partnership", "value": "$50,000 Equity", "deadline": "Past", "description": "Seed fund bridging software solutions and VC funding.", "eligibility": "Early-stage tech startups.", "strategicFit": "Co-host regional pitch events.", "portalUrl": "https://meltwater.org/", "businessAction": ["Align ALX Ventures with MEST."], "matchScore": 90 },
        { "title": "Africa No Filter - Operational Grant", "source": "Africa No Filter", "country": "Pan-African", "type": "Grant", "status": "Open", "sector": "Content Creation", "category": "Business Only", "value": "Up to $25,000", "deadline": "Rolling", "description": "Grants aimed at media organizations changing African narratives.", "eligibility": "Media hubs.", "strategicFit": "Apply for grant to build Digital Storytelling module.", "portalUrl": "https://africanofilter.org/", "businessAction": ["Draft proposal to ANF."], "matchScore": 94 },
        { "title": "Creative Enterprise Support Programme", "source": "British Council", "country": "Nigeria, Kenya", "type": "Training", "status": "Forecast", "sector": "Finance", "category: ": "Business Only", "value": "£50k", "deadline": "Est. Mar 2026", "description": "Business management training for creatives.", "eligibility": "Training providers.", "strategicFit": "ALX as Training Execution Partner.", "portalUrl": "https://britishcouncil.org/", "businessAction": ["Prepare credentials to bid."], "matchScore": 98 },
        { "title": "HEVA Fund - Growth Facility", "source": "HEVA Fund", "country": "Kenya", "type": "Loan", "status": "Open", "sector": "Finance", "category": "Business Only", "value": "Up to $50,000", "deadline": "Rolling", "description": "Working capital for digital media.", "eligibility": "Registered businesses.", "strategicFit": "Financing for ALX alumni agencies.", "portalUrl": "https://hevafund.com/", "businessAction": ["Invite HEVA directors to ALX Nairobi."], "matchScore": 93 },
        { "title": "Netflix Creative Equity Fund", "source": "Netflix", "country": "Pan-African", "type": "Training", "status": "Closed", "sector": "Film & TV", "category": "Business Only", "value": "Full Tuition", "deadline": "Past", "description": "Financial support to African film students.", "eligibility": "Partner institutions.", "strategicFit": "Become official CESF partner.", "portalUrl": "https://netflix.com/", "businessAction": ["Contact Netflix policy team."], "matchScore": 97 },
        { "title": "KZNFC Production Fund", "source": "KZN Film", "country": "South Africa", "type": "Gov Grant", "status": "Urgent", "sector": "Film & TV", "category": "Business Only", "value": "R1,000,000", "deadline": "Feb 28, 2026", "description": "Provincial grant supporting feature films.", "eligibility": "SA production companies.", "strategicFit": "Cloud rendering infrastructure play.", "portalUrl": "https://kznfilm.co.za/", "businessAction": ["Monitor software needs for productions."], "matchScore": 75 }
    ]
    
    print("\n--> [SEED] Injecting Strategic Historical Data...")
    for deal in historical_deals:
        save_to_database(deal)


# ============================================================================
# PHASE 4: RELAXED LIVE SCRAPERS (Grabs Open, Forecast, and Closed deals)
# ============================================================================
def scrape_mastercard_fdn():
    url = "https://mastercardfdn.org/creative-economy/"
    print(f"--> [INST] Scanning Mastercard Foundation: {url}")
    soup = get_soup(url)
    if isinstance(soup, BeautifulSoup):
        text = soup.get_text().lower()
        
        # Determine status based on text instead of ignoring it
        if "request for proposal" in text or "call for applications" in text:
            status = "Open"
        elif "closed" in text or "past programs" in text:
            status = "Closed"
        else:
            status = "Forecast"

        save_to_database({
            "title": "Mastercard Fdn: Creative Tech RFP", "source": "Mastercard Foundation",
            "country": "Pan-African", "type": "Institutional Grant", "status": status,
            "sector": "Tech & Innovation", "category": "Business Only", "value": "$10,000,000+",
            "deadline": "Rolling check", "description": "Automated Scraper tracked the current status of Mastercard's Creative Economy portfolio.",
            "eligibility": "Tier-1 Educational platforms.", "strategicFit": "High capacity building requirements expected.", "portalUrl": url
        })

def scrape_epic_megagrants():
    url = "https://www.unrealengine.com/en-US/megagrants"
    print(f"--> [TECH] Scanning Epic MegaGrants: {url}")
    soup = get_soup(url)
    if isinstance(soup, BeautifulSoup):
        text = soup.get_text().lower()
        
        status = "Open" if "apply now" in text else "Closed"

        save_to_database({
            "title": "Epic MegaGrants Live Scan", "source": "Epic Games",
            "country": "Pan-African", "type": "Tech Grant", "status": status,
            "sector": "Tech & Innovation", "category": "B2B Partnership", "value": "Up to $500k",
            "deadline": "Monitored Daily", "description": "Live status update of the Epic Games portal.",
            "eligibility": "Unreal Engine Developers", "strategicFit": "Pipeline opportunity.", "portalUrl": url
        })


# ============================================================================
# PHASE 5: MAIN EXECUTION LOOP
# ============================================================================
def run_harvester():
    print("\n=======================================================")
    print("🚀 ALX CREATIVE ECONOMY HARVESTER ENGINE INITIATED")
    print("=======================================================\n")
    
    # 1. Inject the historical database
    inject_historical_mock_data()
    time.sleep(2)
    
    # 2. Run the live internet scanners to update statuses
    scrape_mastercard_fdn()
    time.sleep(1)
    scrape_epic_megagrants()
    
    print("\n=======================================================")
    print("✅ HARVESTER CYCLE COMPLETE. DB UPDATED.")
    print("=======================================================\n")

if __name__ == "__main__":
    run_harvester()