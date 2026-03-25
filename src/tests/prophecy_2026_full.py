import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
import swisseph as swe

def analyze_month_2026(year, month, ep):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
    # Sample Middle of Month for General Theme
    mid_date = start_date + timedelta(days=15)
    pos = ep.get_all_positions(mid_date)
    
    theme = "Neutral"
    risk_level = "Low"
    key_event = ""
    sectors = "Balanced"
    
    # --- 1. Jupiter Check (The Great Benefic) ---
    j_lon = pos['Jupiter']
    # Gemini: 60-90, Cancer: 90-120
    if 60 <= j_lon < 90:
        j_sign = "Gemini"
    elif 90 <= j_lon < 120:
        j_sign = "Cancer"
    else:
        j_sign = "Other"
        
    # --- 2. Saturn Check (The Great Malefic) ---
    s_lon = pos['Saturn']
    # Pisces: 330-360
    if 330 <= s_lon <= 360:
        s_sign = "Pisces"
    else:
        s_sign = "Aries" # Late year?
        
    # --- 3. Mars Check (The Trigger) ---
    m_lon = pos['Mars']
    
    # --- Logic Synthesis ---
    
    # JAN - MAR (Jupiter Gemini, Saturn Pisces)
    if month <= 3:
        theme = "The Tech Bubble (Artificial High)"
        risk_level = "Medium-High (Late March)"
        key_event = "Jupiter Trine Pluto/Mercury"
        sectors = "Tech (Bubble), Crypto (Peak)"

    # APRIL (The Crash)
    elif month == 4:
        theme = "The Great Freeze (Saturn-Mars Conjunction)"
        risk_level = "CRITICAL (10/10)"
        key_event = "Saturn Conjunct Mars (Pisces)"
        sectors = "SHORT Energy, SHORT Shipping, Cash is King"
        
    # MAY - JUNE (The Aftermath)
    elif month in [5, 6]:
        theme = "Deflationary Stagnation"
        risk_level = "High (Economic Reality)"
        key_event = "Sun/Venus in Taurus (Slow)"
        sectors = "Consumer Staples (Safety), Gold"
        
        # Check specific Jupiter Ingress
        # In 2026, Jupiter enters Cancer around late Oct? Or Mid Year?
        # Sidereal Jupiter in Gemini until ~Oct 2026? Let's rely on ephemeris in loop
        if j_sign == "Cancer":
            theme = "Recovery Begins (Jupiter Exalted)"
            
    # JULY - SEPT (Stabilization)
    elif month in [7, 8, 9]:
        theme = "The Slow Grind"
        risk_level = "Medium"
        if j_sign == "Cancer":
             theme = "The Golden Revival"
             sectors = "Banking, Real Estate, Education"
        else:
             sectors = "Defense, Utilities"

    # OCT - DEC (The Renaissance?)
    elif month >= 10:
        # Jupiter enters Cancer (Exalted) usually late in year or next year
        if j_sign == "Cancer":
            theme = "A New Golden Age Begins"
            risk_level = "Low (Buy Opportunity)"
            key_event = "Jupiter Exalted in Cancer"
            sectors = "Everything (Especially Banks/Homebuilders)"
        else:
            theme = "Consolidation"
            risk_level = "Medium"
            
    # Refine with Mars Transits
    # Mars in Cap (Exalted) -> Energy Spike
    if 270 <= m_lon <= 300:
        key_event += ", Mars Exalted (Energy Spike)"
        
    # Mars in Can (Debilitated) -> Energy Crash
    if 90 <= m_lon <= 120:
        key_event += ", Mars Debilitated (Energy Slump)"
        
    return {
        "Month": start_date.strftime("%B"),
        "Theme": theme,
        "Risk": risk_level,
        "Key_Event": key_event,
        "Sectors": sectors,
        "Jup_Sign": j_sign,
        "Sat_Sign": s_sign
    }

def run_2026_forecast():
    print("=== Arion.ai 2026 Year-Ahead Prophecy ===")
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    results = []
    print("Scanning Jan-Dec 2026...")
    for m in range(1, 13):
        res = analyze_month_2026(2026, m, ep)
        results.append(res)
        
    # Generate Report
    with open("prophecy_2026_full_year.md", "w", encoding="utf-8") as f:
        f.write("# Arion.ai 2026: The Year of Fire & Ice\n")
        f.write("**Full Year Astrological Roadmap**\n\n")
        
        f.write("## 📅 Executive Summary\n")
        f.write("- **H1 (Jan-Jun):** The \"Tech Bubble\" pops into a \"Deflationary Freeze\". **High Volatility.**\n")
        f.write("- **H2 (Jul-Dec):** A slow reconstruction, leading to a massive **\"Golden Age\" buy signal** in late 2026 when Jupiter enters Cancer (Exalted).\n\n")
        
        f.write("--- \n\n")
        f.write("## 🗓️ Month-by-Month Forecast\n\n")
        
        f.write("| Month | Theme | Risk Level | Key Event | Best Sectors |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        
        for r in results:
            f.write(f"| **{r['Month']}** | {r['Theme']} | {r['Risk']} | {r['Key_Event']} | {r['Sectors']} |\n")
            
        f.write("\n")
        f.write("## 🗝️ The Turning Point: Jupiter in Cancer\n")
        # Find when Jupiter enters Cancer
        cancer_entry = "Not in 2026"
        for r in results:
            if r['Jup_Sign'] == "Cancer":
                cancer_entry = r['Month']
                break
                
        f.write(f"**Jupiter Exaltation Detected:** {cancer_entry}\n")
        f.write("Once Jupiter enters Cancer, the 'Depression' ends. Banks and Real Estate will lead the next multi-year bull run.\n")
        
    print("Forecast Generated: prophecy_2026_full_year.md")

if __name__ == "__main__":
    run_2026_forecast()
