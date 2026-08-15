import swisseph as swe
import pandas as pd
from datetime import datetime, timedelta
import os

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def calculate_lunar_triggers(start_date, end_date):
    print(f"=== ACE: LUNAR TRIGGER CALCULATOR (APR-MAY 2026) ===")
    
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    current = start_date
    triggers = []
    
    # Tikshna (Sharp/Dreadful) Nakshatras - The Crash Amplifiers
    TIKSHNA_NAK = [6, 9, 18, 19] # Ardra, Ashlesha, Jyeshtha, Mula
    
    print(f"Scanning for intersections with Mars, Saturn, and Ketu...")
    
    while current <= end_date:
        jd = swe.julday(current.year, current.month, current.day, current.hour + current.minute/60.0)
        
        # 1. Get Planet Positions
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
        mars_pos = swe.calc_ut(jd, swe.MARS, swe.FLG_SIDEREAL)[0][0]
        saturn_pos = swe.calc_ut(jd, swe.SATURN, swe.FLG_SIDEREAL)[0][0]
        ketu_pos = (swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0] + 180) % 360
        
        # 2. Check Intersections (within 1 degree)
        trigger_found = False
        target = ""
        
        if abs(moon_pos - mars_pos) < 1.0: 
            trigger_found = True; target = "MARS (Velocity)"
        elif abs(moon_pos - saturn_pos) < 1.0: 
            trigger_found = True; target = "SATURN (Structure)"
        elif abs(moon_pos - ketu_pos) < 1.0: 
            trigger_found = True; target = "KETU (Fracture)"
            
        if trigger_found:
            nak = int(moon_pos // (360/27)) + 1
            is_amplified = nak in TIKSHNA_NAK
            
            triggers.append({
                'DateTime': current.strftime('%Y-%m-%d %H:%M'),
                'Target': target,
                'Nakshatra': nak,
                'Is_Amplified': "YES" if is_amplified else "No"
            })
            
        current += timedelta(hours=6) # 6-hour resolution
        
    res_df = pd.DataFrame(triggers)
    print("\n" + "="*70)
    print("THE LUNAR SPARK CALENDAR: APRIL-MAY 2026")
    print("="*70)
    if not res_df.empty:
        # Drop duplicates for the same day to keep it clean
        res_df['Date'] = pd.to_datetime(res_df['DateTime']).dt.date
        res_df = res_df.drop_duplicates(subset=['Date', 'Target'])
        print(res_df[['DateTime', 'Target', 'Is_Amplified']])
    else:
        print("No direct lunar triggers detected in this window.")
    print("="*70)

if __name__ == "__main__":
    start = datetime(2026, 4, 15)
    end = datetime(2026, 5, 15)
    calculate_lunar_triggers(start, end)
