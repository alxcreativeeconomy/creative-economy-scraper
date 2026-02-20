import requests
from bs4 import BeautifulSoup
import time
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# ============================================================================
# PHASE 1: FIREBASE DATABASE INITIALIZATION
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

def save_to_database(deal_data):
    if db is not None:
        try:
            deal_data['tags'] = deal_data.get('tags', []) + ["AI Discovered"]
            db.collection('opportunities').add(deal_data)
            print(f"    [+] Successfully pushed to Firebase: {deal_data['title']}")
        except Exception as e:
            print(f"    [X] Failed to push to Firebase: {e}")
    else:
        print(f"    [SIMULATED PUSH] Found Deal: {deal_data['title']}")

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        elif response.status_code in [403, 401]:
            return "403_PROTECTED"
        return None
    except Exception as e:
        print(f"    [X] Error connecting to {url}: {e}")
        return None

# ============================================================================
# PHASE 3: THE TARGET SCRAPERS
# ============================================================================
def scrape_mastercard_fdn():
    url = "https://mastercardfdn.org/creative-economy/"
    print(f"--> [INST] Scanning Mastercard Foundation: {url}")
    soup = get_soup(url)
    if isinstance(soup, BeautifulSoup) and ("request for proposal" in soup.get_text().lower() or "call for applications" in soup.get_text().lower()):
        print("    [!] RFP Activity Detected!")
        save_to_database({
            "title": "Mastercard Foundation: Active Creative RFP", "source": "Mastercard Foundation",
            "country": "Pan-African", "type": "Institutional Grant", "status": "Urgent",
            "sector": "Tech & Innovation", "category": "Business Only", "value": "Unspecified Mega-Fund",
            "deadline": "Review Immediate", "description": "Automated Scraper detected active RFP keywords.",
            "eligibility": "Tier-1 Educational institutions and EdTech platforms.",
            "strategicFit": "ALX SWEET SPOT. High capacity building requirements expected.", "portalUrl": url
        })

def scrape_epic_megagrants():
    url = "https://www.unrealengine.com/en-US/megagrants"
    print(f"--> [TECH] Scanning Epic MegaGrants: {url}")
    soup = get_soup(url)
    if isinstance(soup, BeautifulSoup) and ("apply now" in soup.get_text().lower() or "submit your project" in soup.get_text().lower()):
        print("    [!] Epic MegaGrants Portal Open!")
        save_to_database({
            "title": "Epic MegaGrants 3D/Animation Funding", "source": "Epic Games",
            "country": "Pan-African", "type": "Tech Grant", "status": "Open",
            "sector": "Tech & Innovation", "category": "B2B Partnership", "value": "$5,000 - $500,000",
            "deadline": "Rolling", "description": "Portal is actively accepting submissions.",
            "eligibility": "Studios and developers using Unreal Engine.",
            "strategicFit": "Pipeline opportunity for ALX Software Engineering graduates.", "portalUrl": url
        })

def scrape_canex():
    url = "https://canex.africa/"
    print(f"--> [FIN] Scanning Afreximbank CANEX: {url}")
    soup = get_soup(url)
    if isinstance(soup, BeautifulSoup) and "deal room" in soup.get_text().lower() and "apply" in soup.get_text().lower():
        print("    [!] CANEX Deal Room activity detected.")

def scrape_heva_fund():
    url = "https://www.hevafund.com/"
    print(f"--> [FIN] Scanning HEVA Fund: {url}")
    soup = get_soup(url)
    if isinstance(soup, BeautifulSoup) and "apply" in soup.get_text().lower():
        print("    [!] HEVA Fund facility is OPEN.")

def scrape_africa_no_filter():
    url = "https://africanofilter.org/grants"
    print(f"--> [GRANT] Scanning Africa No Filter: {url}")
    soup = get_soup(url)
    if isinstance(soup, BeautifulSoup) and "applications are open" in soup.get_text().lower():
        print("    [!] Africa No Filter grants portal active.")

def scrape_mest_africa():
    url = "https://meltwater.org/"
    print(f"--> [TECH] Scanning MEST Africa: {url}")
    soup = get_soup(url)
    if isinstance(soup, BeautifulSoup) and "challenge" in soup.get_text().lower():
        print("    [!] MEST Africa program activity detected.")

# ============================================================================
# PHASE 4: MAIN EXECUTION LOOP
# ============================================================================
def run_harvester():
    print("\n=======================================================")
    print("🚀 ALX CREATIVE ECONOMY HARVESTER ENGINE INITIATED")
    print("=======================================================\n")
    scrape_mastercard_fdn()
    time.sleep(1)
    scrape_epic_megagrants()
    time.sleep(1)
    scrape_canex()
    time.sleep(1)
    scrape_heva_fund()
    time.sleep(1)
    scrape_africa_no_filter()
    time.sleep(1)
    scrape_mest_africa()
    print("\n=======================================================")
    print("✅ HARVESTER CYCLE COMPLETE. DB UPDATED.")
    print("=======================================================\n")

if __name__ == "__main__":
    run_harvester()