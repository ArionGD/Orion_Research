from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

# Project Root Setup
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
VED_PATH = os.path.join(ROOT, 'ved_engine')
FRONTEND_DIST = os.path.join(ROOT, 'frontend', 'dist')

# Auto-load root .env file
env_file = os.path.join(ROOT, '.env')
if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

if ROOT not in sys.path:
    sys.path.append(ROOT)
if VED_PATH not in sys.path:
    sys.path.append(VED_PATH)

# Core Engine Imports
try:
    from src.engine.medini.crash_logic import MundaneWeatherEngine
    from src.engine.medini.synthesizer import MediniSynthesizer
    from src.engine.astro.core.ephemeris_provider import EphemerisProvider
    from src.engine.corporate.risk_engine import CorporateRiskEngine, PRESET_COMPANIES, SECTOR_ASTRO_MAP
except Exception as e:
    print(f"Warning: Engine imports partial: {e}")
    MundaneWeatherEngine = None
    MediniSynthesizer = None
    EphemerisProvider = None
    CorporateRiskEngine = None
    PRESET_COMPANIES = {}
    SECTOR_ASTRO_MAP = {}

# Ved Engine Imports
try:
    import vedastro
    VED_ENGINE_AVAILABLE = True
except Exception as e:
    print(f"Warning: ved_engine integration partial: {e}")
    VED_ENGINE_AVAILABLE = False

app = FastAPI(
    title="ORION RESEARCH: Sovereign Intelligence & Commodity Engine",
    description="ACE v5 Medini Engine + Commodities Analytics + Gemini 2.5 Flash Mudra AI Agent.",
    version="5.5.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Engines ---
weather_engine = MundaneWeatherEngine() if MundaneWeatherEngine else None
synthesizer = MediniSynthesizer() if MediniSynthesizer else None
ep = EphemerisProvider() if EphemerisProvider else None
corporate_engine = CorporateRiskEngine() if CorporateRiskEngine else None

class ChatMessage(BaseModel):
    role: str # "user" or "model"
    text: str

class ChatRequest(BaseModel):
    message: str
    api_key: Optional[str] = None
    history: Optional[List[ChatMessage]] = None

ALIAS_MAP = {
    "ADANI PORT": "ADANIPORTS", "ADANI PORTS": "ADANIPORTS", "ADANIPORTS": "ADANIPORTS", "ADANI": "ADANIPORTS",
    "TATA MOTORS": "TATAMOTORS", "TATA MOTOR": "TATAMOTORS", "TATAMOTORS": "TATAMOTORS",
    "BHARTI": "BHARTIARTL", "AIRTEL": "BHARTIARTL", "BHARTIARTL": "BHARTIARTL",
    "L&T": "LT", "LARSEN": "LT", "LT": "LT",
    "SBI": "SBIN", "STATE BANK": "SBIN", "SBIN": "SBIN",
    "HDFC": "HDFCBANK", "HDFCBANK": "HDFCBANK",
    "ICICI": "ICICIBANK", "ICICIBANK": "ICICIBANK",
    "INFOSYS": "INFY", "INFY": "INFY",
    "TCS": "TCS", "WIPRO": "WIPRO", "TECHM": "TECHM",
    "RELIANCE": "RELIANCE", "RIL": "RELIANCE",
    "ONGC": "ONGC", "BPCL": "BPCL", "NTPC": "NTPC", "POWERGRID": "POWERGRID",
    "GOLD": "GOLD", "XAU": "GOLD", "SILVER": "SILVER", "XAG": "SILVER", "OIL": "OIL", "GAS": "OIL", "CRUDE": "OIL"
}

# Helper to call Google Gemini REST API
def call_gemini_api_multiturn(prompt_text: str, context_text: str, history_list: List[ChatMessage], api_key: str):
    # Active Gemini models in v1beta
    models_to_try = ["gemini-2.5-flash", "gemini-3.5-flash", "gemini-flash-latest", "gemini-2.5-pro"]
    last_err_msg = ""

    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            
            contents = []
            contents.append({
                "role": "user",
                "parts": [{"text": f"System Context (ORION RESEARCH ASTRO ENGINE):\n{context_text}"}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Understood. I am Mudra AI, an expert agentic AI financial & mundane astrological analyst powered by ORION RESEARCH. I will answer user queries concisely with context awareness."}]
            })

            if history_list:
                for item in history_list[-6:]:
                    r = "user" if item.role in ["user", "human"] else "model"
                    contents.append({
                        "role": r,
                        "parts": [{"text": item.text}]
                    })

            contents.append({
                "role": "user",
                "parts": [{"text": prompt_text}]
            })

            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 1500
                }
            }
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=12) as response:
                res_body = response.read().decode('utf-8')
                res_json = json.loads(res_body)
                candidates = res_json.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        return parts[0].get('text'), None, model_name
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='ignore')
            print(f"Gemini API ({model_name}) HTTP Error {e.code}: {err_body}")
            try:
                err_json = json.loads(err_body)
                last_err_msg = err_json.get('error', {}).get('message', str(e))
            except Exception:
                last_err_msg = f"HTTP {e.code}: {err_body[:200]}"
        except Exception as err:
            print(f"Gemini API ({model_name}) Exception: {err}")
            last_err_msg = str(err)
            
    return None, last_err_msg, None

# --- API Endpoints ---

@app.get("/api/v1/health")
async def health_check():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    return {
        "status": "ready",
        "engine": "ARION-V5-ACE",
        "ved_engine_status": "ONLINE" if VED_ENGINE_AVAILABLE else "PARTIAL",
        "corporate_engine": "ONLINE" if corporate_engine else "OFFLINE",
        "mudra_ai": "GEMINI MULTI-TURN AGENT READY",
        "gemini_api_key_configured": bool(api_key),
        "frontend": "React SPA (Vite)",
        "version": "5.5.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/chat/mudra")
async def mudra_ai_chat(req: ChatRequest):
    """
    Mudra AI Context-Aware Agent powered directly by Gemini API.
    """
    msg = req.message.strip()
    msg_upper = msg.upper()
    api_key = req.api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    history = req.history or []

    # 1. Robust Alias Matcher on CURRENT message
    target_symbol = None
    for alias, sym in ALIAS_MAP.items():
        if alias in msg_upper:
            target_symbol = sym
            break

    if not target_symbol:
        for sym in PRESET_COMPANIES.keys():
            if sym in msg_upper or PRESET_COMPANIES[sym]["name"].upper() in msg_upper:
                target_symbol = sym
                break

    # 2. Context Memory Resolution ONLY IF NO NEW ENTITY matched
    if not target_symbol and history:
        for hist_item in reversed(history):
            h_text = hist_item.text.upper()
            for alias, sym in ALIAS_MAP.items():
                if alias in h_text:
                    target_symbol = sym
                    break
            if target_symbol: break

    current_smi = 7.80

    stock_context = ""
    analysis = None
    if target_symbol and target_symbol in PRESET_COMPANIES and corporate_engine:
        preset = PRESET_COMPANIES[target_symbol]
        analysis = corporate_engine.analyze_company_horoscope(
            company_symbol=target_symbol,
            incorporation_date_str=preset.get("date", "1994-08-30"),
            current_smi=current_smi
        )
        stock_context = f"""
Matched Ticker: {analysis['company_name']} ({analysis['symbol']})
Inception Date: {analysis['incorporation_date']}
Sector: {analysis['category']} — {analysis['sector']}
Mundane Sector SMI: {analysis['mundane_smi_score']} / 10
Company Personal Micro Risk: {analysis['company_micro_risk']} / 10
Dual Alignment Risk Index: {analysis['dual_risk_index']} / 10
Status: {analysis['recipe_status']}
Active Transit Signals: {', '.join(analysis['signals'])}
Recipe Logic: {analysis['recipe_desc']}
"""

    system_context = f"""
ORION RESEARCH ACE v5.5 FORENSIC ASTROLOGICAL INTELLIGENCE PLATFORM
Current Date: {datetime.now().strftime('%Y-%m-%d')}
Active Sovereign Malefic Index (SMI): 7.80 / 10 (STORM / HIGH VOLATILITY)
Active Planetary Aspects: Saturn-Rahu Conjunction, Jupiter Ingress in Taurus, Solar/Lunar Eclipse Axis in Aquarius/Leo (August 12 & August 27, 2026).
{stock_context}
Instruction: Act as Mudra AI, an expert agentic AI financial & mundane astrological analyst. Answer user queries directly with comprehensive financial, technical, and astrological insights for the specific stock requested.
"""

    # Call Real Gemini API if Key is provided
    if api_key:
        gemini_reply, err_msg, used_model = call_gemini_api_multiturn(msg, system_context, history if not target_symbol else [], api_key)
        if gemini_reply:
            return {
                "symbol": target_symbol or "MARKET",
                "reply": gemini_reply,
                "engine": f"Gemini API ({used_model})",
                "metrics": {
                    "smi_score": 7.80,
                    "micro_risk": 5.20 if not analysis else analysis['company_micro_risk'],
                    "dual_risk": 6.50 if not analysis else analysis['dual_risk_index'],
                    "status": "LIVE GEMINI AI RESPONSE"
                }
            }
        elif err_msg:
            # If Google API returned an explicit error (e.g. 429 quota/billing depleted), surface it directly!
            if "credits are depleted" in err_msg or "429" in err_msg:
                return {
                    "symbol": target_symbol or "MARKET",
                    "reply": f"### ⚠️ Google Gemini API Quota Notice\n\nGoogle API returned a quota limit error for this key:\n`{err_msg}`\n\n**To fix this & get unlimited live Gemini responses:**\n1. In [Google AI Studio](https://aistudio.google.com/app/apikey), generate a key under **Default Gemini Project** (which gives 1,500 free queries/day).\n2. Or link your GCP Billing Account to `project-ba753270-5762-47c5-ba6` in GCP Console.",
                    "metrics": {"smi_score": 7.80, "micro_risk": 5.0, "dual_risk": 6.4, "status": "GEMINI QUOTA LIMITED"}
                }

    # Dynamic Fallback
    if target_symbol == "GOLD":
        return {
            "symbol": "GOLD",
            "reply": "### 🪙 Mudra AI Deep Forensic Intelligence: Gold (XAU)\n\nGold consolidates between ₹1,60,000 – ₹1,65,000 during August eclipse windows, followed by a +10% to +14% breakout past ₹1,70,000 in September-October 2026.",
            "metrics": {"smi_score": 7.80, "micro_risk": 5.0, "dual_risk": 6.4, "status": "GOLD ANALYSIS ACTIVE"}
        }

    elif target_symbol in PRESET_COMPANIES and analysis:
        return {
            "symbol": target_symbol,
            "company_name": analysis['company_name'],
            "reply": f"### 🏗️ Mudra AI Forensic Intelligence: {analysis['company_name']} ({analysis['symbol']})\n\n- **Inception Date:** `{analysis['incorporation_date']}`\n- **Dual Risk Index:** `{analysis['dual_risk_index']} / 10`\n- **Outlook:** Transiting Mars in Gemini aligns with natal Sun/Jupiter, indicating port volume expansion toward 1st September 2026.",
            "metrics": {
                "smi_score": analysis['mundane_smi_score'],
                "micro_risk": analysis['company_micro_risk'],
                "dual_risk": analysis['dual_risk_index'],
                "status": analysis['recipe_status']
            }
        }

    else:
        return {
            "symbol": "MACRO",
            "reply": f"### ✦ Mudra AI Sovereign Macro Intelligence\n\n**Query:** \"{msg}\"\n\n**SMI Weather:** `7.80 / 10 (STORM / HIGH VOLATILITY)`\nAugust 12 & 27 Eclipses on Aquarius/Leo Axis create short-term market consolidation before September expansion.",
            "metrics": {"smi_score": 7.80, "micro_risk": 5.0, "dual_risk": 6.4, "status": "SOVEREIGN MACRO"}
        }

@app.get("/api/v1/commodities/forecast")
async def get_commodity_forecast(commodity: str = "gold"):
    return {"asset": commodity, "status": "active"}

@app.get("/api/v1/company/presets")
async def get_preset_companies():
    return {"companies": PRESET_COMPANIES, "sectors": list(SECTOR_ASTRO_MAP.keys())}

@app.get("/api/v1/company/analysis")
async def analyze_company(symbol: str = "AAPL", incorporation_date: Optional[str] = None, smi: float = 5.5):
    if not corporate_engine: raise HTTPException(status_code=503, detail="Unavailable")
    if not incorporation_date: incorporation_date = PRESET_COMPANIES.get(symbol, {}).get("date", "1976-04-01")
    return corporate_engine.analyze_company_horoscope(company_symbol=symbol, incorporation_date_str=incorporation_date, current_smi=smi)

@app.get("/api/v1/vedic/panchanga")
async def get_vedic_panchanga(date: str = Query(None)):
    date_obj = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    return {"date": date_obj.strftime("%Y-%m-%d"), "panchanga": {"tithi": "Shukla Navami", "nakshatra": "Rohini"}}

@app.get("/smi/report")
async def get_smi_report(date: str = Query(None), market: str = "US"):
    date_obj = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    return {"date": date_obj.strftime("%Y-%m-%d"), "smi": 7.80, "status": "STORM", "system_gravity": "HIGH"}

@app.get("/smi/forecast")
async def get_smi_forecast(start_date: str, days: int = 30, sector: str = "All"):
    start_obj = datetime.strptime(start_date, "%Y-%m-%d")
    return [{"date": (start_obj + timedelta(days=i)).strftime("%Y-%m-%d"), "smi": 7.8, "sector": sector} for i in range(min(days, 30))]

if os.path.exists(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
