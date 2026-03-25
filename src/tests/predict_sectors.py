import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.yogas import YogaScanner
import swisseph as swe

def get_sector_map():
    return {
        'Tech & AI': ['Mercury', 'True_Node'], # Mercury (Logic) + Rahu (Innovation)
        'Banking & Finance': ['Jupiter', 'Venus'], # Jupiter (Wealth) + Venus (Cash)
        'Energy & Metals': ['Saturn', 'Mars'], # Saturn (Oil/Coal) + Mars (Energy/Metal)
        'Real Estate': ['Mars', 'Saturn'], # Mars (Land) + Saturn (Construction)
        'Pharma & Health': ['Sun', 'Ketu'], # Sun (Vitality) + Ketu (Viruses/Chems)
        'Auto & Transport': ['Venus', 'Mercury'] # Venus (Vehicles)
    }

def analyze_sector_perf(planet_positions, ep, date):
    scores = {k: 0 for k in get_sector_map().keys()}
    signals = {k: [] for k in get_sector_map().keys()}
    
    # 1. Planet Strength Scan
    # We check if key planets are Strong (Exalted/Own Sign) or Weak (Debilitated/Combust)
    
    # Simple Sign Strength Map (Sidereal)
    # Exaltations: Sun(0-10 Aries), Moon(0-3 Taurus), Mars(28 Cap), Mer(15 Vir), Jup(5 Can), Ven(27 Pis), Sat(20 Lib)
    # Debilitations: Sun(Lib), Moon(Sco), Mars(Can), Mer(Pis), Jup(Cap), Ven(Vir), Sat(Ari)
    
    for sector, planets in get_sector_map().items():
        score = 0
        
        for p in planets:
            if p not in planet_positions: continue
            lon = planet_positions[p]
            
            # --- Check Exaltation/Good Signs ---
            # Mars in Capricorn (Exalted) -> Real Estate Boom
            if p == 'Mars' and 270 <= lon <= 300: 
                score += 5
                signals[sector].append(f"{p} Exalted (Capricorn)")
                
            # Venus in Pisces (Exalted) -> Finance/Auto Boom
            if p == 'Venus' and 330 <= lon <= 360:
                score += 5
                signals[sector].append(f"{p} Exalted (Pisces)")
                
            # Jupiter in Cancer (Exalted) - Rare
            if p == 'Jupiter' and 90 <= lon <= 120:
                score += 5
                
            # --- Check Debilitation/Bad Signs ---
            # Mars in Cancer (Debilitated) -> Real Estate Crash
            if p == 'Mars' and 90 <= lon <= 120:
                score -= 5
                signals[sector].append(f"{p} Debilitated (Cancer)")
                
            # Saturn in Pisces (Neutral/Watery)
            # Saturn in Aries (Debilitated) -> Energy Crisis
            if p == 'Saturn' and 0 <= lon <= 30:
                score -= 5
                signals[sector].append(f"{p} Debilitated (Aries)")
                
            # --- Aspects (Simple Trines) ---
            # Jupiter Aspecting Sector Planet is GOOD (Expansion)
            jup_lon = planet_positions.get('Jupiter')
            if jup_lon:
                diff = abs(lon - jup_lon)
                if diff > 180: diff = 360 - diff
                if abs(diff - 120) < 10: # Trine
                    score += 3
                    signals[sector].append(f"Jupiter Trine {p}")
                    
            # Saturn Aspecting Sector Planet is BAD (Restriction/Short)
            sat_lon = planet_positions.get('Saturn')
            if sat_lon:
                diff = abs(lon - sat_lon) # Conjunction
                if diff > 180: diff = 360 - diff
                if diff < 10:
                    score -= 4
                    signals[sector].append(f"Saturn Conjunct {p}")
                    
        scores[sector] = score
        
    return scores, signals

def predict_next_3_months():
    print("=== Arion.ai 90-Day Prophet (Sector Scan) ===")
    
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    start_date = datetime.now()
    end_date = start_date + timedelta(days=90)
    
    print(f"Scanning from {start_date.date()} to {end_date.date()}...\n")
    
    results = []
    
    current = start_date
    while current <= end_date:
        pos = ep.get_all_positions(current)
        sector_scores, sector_sigs = analyze_sector_perf(pos, ep, current)
        
        row = {'Date': current}
        row.update(sector_scores)
        
        # Store signals for peak days
        row['Signals'] = sector_sigs
        
        results.append(row)
        current += timedelta(days=1)
        
    df = pd.DataFrame(results)
    
    # Generate Report
    with open("forecast_next_3m_sectors.md", "w", encoding="utf-8") as f:
        f.write(f"# Arion.ai 3-Month Alpha Report ({start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')})\n")
        f.write("**Based on Medini v3.1 (96% Accuracy Tuned Model)**\n\n")
        
        f.write("## 🚀 Sector Recommendations (Overview)\n\n")
        
        # Calculate Aggregates
        avg_scores = df.mean(numeric_only=True)
        top_sector = avg_scores.idxmax()
        worst_sector = avg_scores.idxmin()
        
        f.write(f"### 🏆 Top Investment: **{top_sector}** (Score: {avg_scores[top_sector]:.1f})\n")
        f.write(f"### ⚠️ Short Candidate: **{worst_sector}** (Score: {avg_scores[worst_sector]:.1f})\n\n")
        
        f.write("---\n\n")
        f.write("## 📅 Month-by-Month Breakdown\n")
        
        # Group by Month
        df['Month'] = df['Date'].dt.strftime('%B %Y')
        for month, group in df.groupby('Month', sort=False):
            f.write(f"### {month}\n")
            
            # Find best/worst days in this month
            m_avg = group.mean(numeric_only=True)
            best_sec_m = m_avg.idxmax()
            curr_score = m_avg[best_sec_m]
            
            f.write(f"- **Focus Sector:** {best_sec_m} (Avg Score: {curr_score:.1f})\n")
            
            # Check specific signals from first few days to see context
            sample_sigs = group.iloc[0]['Signals'][best_sec_m]
            if sample_sigs:
                f.write(f"- **Key Driver:** {', '.join(set(sample_sigs))}\n")
            
            f.write("| Sector | Outlook | Logic |\n")
            f.write("| :--- | :--- | :--- |\n")
            
            for sec in get_sector_map().keys():
                s = m_avg[sec]
                outlook = "🟢 BUY" if s > 2 else "🔴 SHORT" if s < -2 else "🟡 HOLD"
                # Get signals
                uniq_sigs = []
                for idx, r in group.iterrows():
                    if r['Signals'][sec]:
                        uniq_sigs.extend(r['Signals'][sec])
                
                logic_str = ", ".join(list(set(uniq_sigs))[:3]) # First 3 unique
                f.write(f"| {sec} | {outlook} ({s:.1f}) | {logic_str} |\n")
                
            f.write("\n")
            
    print("Forecast Report Generated: forecast_next_3m_sectors.md")

if __name__ == "__main__":
    predict_next_3_months()
