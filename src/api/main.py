from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import os
import sys

# Project Root Setup
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# Core Engine Imports
from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.medini.synthesizer import MediniSynthesizer
from src.engine.astro.core.ephemeris_provider import EphemerisProvider

app = FastAPI(
    title="ARION CORE: Sovereign Intelligence API",
    description="The High-Performance Backend for the ACE v5 Medini Engine.",
    version="5.5.0"
)

# Enable CORS for Phoenix Dashboard (Local/Prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Engines ---
weather_engine = MundaneWeatherEngine()
synthesizer = MediniSynthesizer()
ep = EphemerisProvider()

# --- Models ---
class SMIReport(BaseModel):
    date: str
    smi_score: float
    status: str
    geopol_intensity: float
    recommendation: str

# --- Endpoints ---

@app.get("/")
async def health_check():
    """ACE Engine Health & Sovereign Connectivity."""
    return {
        "status": "ready",
        "engine": "ARION-V5-ACE",
        "version": "5.5.0",
        "mode": "Sovereign Purity"
    }

@app.get("/smi/report", response_model=Dict)
async def get_smi_report(
    date: str = Query(None, description="ISO Date (YYYY-MM-DD). Defaults to Today."),
    market: str = "US"
):
    """
    Returns the Sovereign Malefic Index (SMI) and Full Forensic Report.
    Target: High-Performance Dashboard Integration.
    """
    try:
        if not date:
            date_obj = datetime.now()
        else:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        
        # 1. Gather Engine Data
        positions = ep.get_all_positions(date_obj)
        
        # Determine Dasha Context (In a real app, from a dasha_registry or country_manager)
        # Proxying for dashboard logic consistency
        dasha_md = "Saturn" if date_obj.year >= 2026 else "Jupiter"
        dasha_ad = "Rahu" if date_obj.month in [4, 9, 10] else "Venus"
        
        smi_data = weather_engine.get_weather_report(date_obj, positions, dasha_md, dasha_ad)
        detailed_report = synthesizer.generate_medini_report(date_obj)
        
        return {
            "date": date_obj.strftime("%Y-%m-%d"),
            "market": market,
            "smi": smi_data['Sovereign_Malefic_Index'],
            "status": smi_data['Astro_Weather_Status'],
            "forensic_report": detailed_report,
            "system_gravity": "HIGH" if smi_data['Sovereign_Malefic_Index'] >= 7.0 else "NORMAL"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/smi/forecast", response_model=List[Dict])
async def get_smi_forecast(
    start_date: str,
    days: int = 30
):
    """
    Forensic Forecast: SMI Trend for the next N days.
    Perfect for Charting the 'Strike Peak' on the dashboard.
    """
    try:
        start_obj = datetime.strptime(start_date, "%Y-%m-%d")
        forecast = []
        
        for i in range(days):
            current_date = start_obj.replace(day=start_obj.day + i) # Simplified increment
            # Real increment handling logic
            from datetime import timedelta
            current_date = start_obj + timedelta(days=i)
            
            positions = ep.get_all_positions(current_date)
            # Dasha proxies
            d_md = "Saturn" if current_date.year >= 2026 else "Jupiter"
            d_ad = "Rahu" if current_date.month in [4, 9, 10] else "Venus"
            
            smi_score = weather_engine.calculate_smi(current_date, positions, d_md, d_ad)
            
            forecast.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "smi": round(smi_score, 2)
            })
            
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
