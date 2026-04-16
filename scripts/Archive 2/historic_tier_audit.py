import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import swisseph as swe

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
sys.path.append(ROOT)

from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def identify_historic_crashes(df):
    """Identifies and groups unique drawdown events into Tiers."""
    df['Peak'] = df['Close'].rolling(window=252, min_periods=100).max()
    df['Drawdown'] = (df['Close'] - df['Peak']) / df['Peak']
    
    events = []
    current_event = None
    
    for date, row in df.iterrows():
        dd = row['Drawdown']
        if dd <= -0.05:
            if current_event is None:
                current_event = {'Start': date, 'Max_DD': dd, 'Date_Max': date}
            else:
                if dd < current_event['Max_DD']:
                    current_event['Max_DD'] = dd
                    current_event['Date_Max'] = date
        else:
            if current_event:
                # Close out event
                mdd = abs(current_event['Max_DD'])
                tier = 3 if mdd >= 0.20 else 2 if mdd >= 0.10 else 1
                events.append({'Tier': tier, 'Bottom': current_event['Date_Max'], 'Mag': mdd})
                current_event = None
    return pd.DataFrame(events)

def run_historic_audit(name, start_y, end_y):
    print(f"\nACE {name} Audit: {start_y} - {end_y}")
    print("="*60)
    
    # 1. Setup Engines
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_engine = VimshottariDasha()
    
    # Natal US (S&P 500 Proxy)
    US_MOON = 348.0
    US_BIRTH = datetime(1957, 3, 4)
    
    # 2. Load Data
    csv_path = os.path.join(ROOT, 'data', 'raw', 'US/MASTER/SP500_STANDARD.csv')
    df = pd.read_csv(csv_path, parse_dates=['Date'])
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    df = df[(df['Date'] >= f'{start_y}-01-01') & (df['Date'] <= f'{end_y}-12-31')].copy()
    df.set_index('Date', inplace=True)
    
    # 3. Identify Ground Truth
    crashes = identify_historic_crashes(df)
    
    tier_counts = {1:0, 2:0, 3:0}
    tier_caught = {1:0, 2:0, 3:0}
    
    lead_times = []
    
    for idx, crash in crashes.iterrows():
        t = crash['Tier']
        bottom = crash['Bottom']
        tier_counts[t] += 1
        
        # Check Lead Window (90 days)
        window = pd.date_range(start=bottom - pd.Timedelta(days=90), end=bottom, freq='D')
        was_caught = False
        signal_date = None
        
        for d in window:
            d_obj = d.to_pydatetime()
            pos = ep.get_all_positions(d_obj)
            dashas = dasha_engine.get_current_dasha(US_MOON, US_BIRTH, d_obj)
            
            smi = weather.calculate_smi(d_obj, pos, dashas['Mahadasha'], dashas['Antardasha'], market='US')
            
            threshold = 6.0 if t==3 else 4.0 if t==2 else 2.0
            if smi >= threshold:
                was_caught = True
                signal_date = d_obj # First day the signal fired
                break
        
        if was_caught: 
            tier_caught[t] += 1
            lead_days = (bottom - signal_date).days
            lead_times.append(lead_days)

    # Statistics
    avg_lead = np.mean(lead_times) if lead_times else 0
    std_lead = np.std(lead_times) if lead_times else 0

    # Report
    print(f"{'TIER':<10} | {'TOTAL':<8} | {'CAUGHT':<8} | {'RECALL'}")
    print("-" * 60)
    for t in [3, 2, 1]:
        recall = (tier_caught[t] / tier_counts[t] * 100) if tier_counts[t] > 0 else 0
        print(f"Tier {t:<5} | {tier_counts[t]:<8} | {tier_caught[t]:<8} | {recall:.1f}%")
        
    print(f"\nTIMING ACCURACY (Lead Time):")
    print(f"> Average Lead Time: {avg_lead:.1f} days before bottom")
    print(f"> Timing Variance: +/- {std_lead:.1f} days")
    print(f"> Suggested Strike Window: {int(avg_lead - std_lead)} to {int(avg_lead + std_lead)} days lead.\n")

if __name__ == "__main__":
    # Part 1: 1950 - 2000
    run_historic_audit("Golden Age", 1950, 2000)
    
    # Part 2: 2000 - 2025
    run_historic_audit("Sovereign Age", 2000, 2025)
