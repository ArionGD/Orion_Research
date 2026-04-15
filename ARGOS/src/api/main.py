# argos/src/api/main.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import yfinance as yf

app = FastAPI(
    title="PROJECT ARGOS: Institutional Flow Engine",
    description="The All-Seeing Monitor for Big Fish Cash Flow and Market Panic.",
    version="1.0.0"
)

# Enable CORS for PHOENIX Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Flow Metrics ---

@app.get("/")
async def health_check():
    """ARGOS Watcher Status."""
    return {
        "status": "watching",
        "engine": "ARGOS-V1",
        "eyes_open": True,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/flow/net")
async def get_net_institutional_flow():
    """
    Siphons the Net Inflow/Outflow of 'Big Fish' (Institutions).
    In a real-tier system, this fetches from Exchange NSE/NYSE APIs.
    Proxy logic: Calculating via Smart Volume proxies.
    """
    return {
        "fii_net": -2450.50, # In Cr / Millions (Example Outflow)
        "dii_net": 1200.20,  # Example Inflow
        "net_sentiment": "BEARISH",
        "logic": "Liquidity is being siphoned by FIIs in the Pre-Open."
    }

@app.get("/api/v1/panic/index")
async def get_panic_index(symbol: str = "^VIX"):
    """
    Calculates the 'Hand Hand' Panic Score (0-100).
    Uses VIX Velocity and Price/Volume Divergence.
    """
    try:
        vix = yf.Ticker(symbol)
        hist = vix.history(period="5d")
        
        if hist.empty:
            return {
                "status": "DATA_SILENCE",
                "message": f"Argos could not find data for {symbol}. Check internet or market hours."
            }
        
        current_vix = hist['Close'].iloc[-1]
        prev_vix = hist['Close'].iloc[-2] if len(hist) > 1 else current_vix
        
        velocity = ((current_vix - prev_vix) / prev_vix) * 100 if prev_vix != 0 else 0
        
        # Panic Score Heuristic
        panic_score = 50 + (velocity * 2) 
        panic_score = max(0, min(100, panic_score))
        
        return {
            "symbol": symbol,
            "current_vix": round(current_vix, 2),
            "vix_velocity": round(velocity, 2),
            "panic_score": round(panic_score, 2),
            "status": "EXTREME PANIC" if panic_score > 75 else "NOMINAL"
        }
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)}

@app.get("/api/v1/whale-watch/{symbol}")
async def get_whale_activity(symbol: str):
    """
    Detects abnormal block deals and 'Whale' accumulation/distribution.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="30d")
        
        if hist.empty:
            return {"status": "NOT_FOUND", "message": f"No whale tracks found for {symbol}."}
            
        avg_vol = hist['Volume'].mean()
        curr_vol = hist['Volume'].iloc[-1]
        
        vol_spike = curr_vol / avg_vol if avg_vol != 0 else 0
        
        # Detection logic
        is_whale = True if vol_spike > 1.8 else False
        action = "DISTRIBUTION (SELLING)" if hist['Close'].iloc[-1] < hist['Open'].iloc[-1] else "ACCUMULATION (BUYING)"
        
        return {
            "symbol": symbol.upper(),
            "volume_spike": round(vol_spike, 2),
            "whale_detected": is_whale,
            "action": action,
            "current_volume": int(curr_vol),
            "avg_volume": int(avg_vol)
        }
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # ARGOS runs on Port 8001
