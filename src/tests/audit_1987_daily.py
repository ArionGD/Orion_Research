import pandas as pd
import joblib
import sys
import os

# Ensure src in pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from src.engine.planets.saturn.conjunctions import SaturnConjunctions
from src.engine.planets.mars.general import MarsGeneralLogic
from src.engine.world.havoc_logic import GlobalHavocLogic
from src.engine.world.speculation_logic import SpeculationLogic
from src.engine.astro.core.ephemeris_provider import EphemerisProvider

def audit_1987_daily():
    print("Auditing October 1987 - Daily Resolution...")
    
    # Initialize Engines
    sn_engine = SaturnConjunctions()
    mars_engine = MarsGeneralLogic()
    gh_engine = GlobalHavocLogic()
    spec_engine = SpeculationLogic()
    ep = EphemerisProvider()
    
    # Load Model
    model = joblib.load('models/arion_v1.pkl')
    
    feature_cols = [
        'Saturn_Neptune_Angle', 'is_hard_aspect', 'aspect_intensity', 'is_applying', 
        'retrograde_count', 'Global_Stability_Index', 'Havoc_Velocity', 
        'Havoc_Alert_Level', 'Mars_Volatility_Score', 'Flash_Crash_Probability', 
        'is_uranus_stationary', 'is_hard_flash',
        'Saturn_Speed', 'Neptune_Speed', 'Mars_Speed', 
        'Jupiter_Speed', 'Uranus_Speed', 'Pluto_Speed'
    ]
    other_outers = ['Jupiter', 'Uranus', 'Pluto']

    start_date = datetime(1987, 10, 1)
    results = []
    
    print(f"{'DATE':<12} | {'Flash Prob':<10} | {'Risk':<8}")
    print("-" * 40)
    
    for i in range(31):
        date = start_date + timedelta(days=i)
        prev_date = date - timedelta(days=1)
        
        row = {}
        row.update(sn_engine.analyze_neptune_relation(date, prev_date))
        row.update(mars_engine.calculate_volatility(date))
        row.update(gh_engine.calculate_havoc_features(date, prev_date))
        # Note: calling internal calculation for daily single-day snapshot would be better
        # But spec_engine.calculate_speculation_features scans 30 days ahead by default.
        # We need INSTANTANEOUS flash probability for a daily chart.
        # So we'll implement a local check or just rely on the scanning one 
        # (which returns max prob in the next 30 days). 
        # Actually, for a daily chart, we want 'Is there a flash trigger TODAY?'.
        # The scan is good for monthly aggregation. 
        # Let's do a trick: we want to know if the condition is active TODAY.
        # I will manually check the condition here for precision.
        
        # Manual Instant Check
        v_lon, _, _ = ep.get_planet_data(date, 'Venus')
        u_lon, u_speed, _ = ep.get_planet_data(date, 'Uranus')
        dist = ep.get_distance(v_lon, u_lon)
        
        dist_0 = abs(dist - 0)
        dist_90 = abs(dist - 90)
        dist_180 = abs(dist - 180)
        is_major = min(dist_0, dist_90, dist_180) <= 3.0
        
        dist_45 = abs(dist - 45)
        dist_135 = abs(dist - 135)
        is_minor = min(dist_45, dist_135) <= 2.0
        
        is_stat = abs(u_speed) < 0.02
        
        raw_score = 0
        if is_major: raw_score += 0.5
        elif is_minor: raw_score += 0.4
        
        if is_stat: 
            raw_score += 0.4
            if (is_major or is_minor): raw_score += 0.1
            
        prob = min(1.0, raw_score)
        
        row['Flash_Crash_Probability'] = prob
        row['is_uranus_stationary'] = 1 if is_stat else 0
        row['is_hard_flash'] = 1 if (is_major or is_minor) else 0
        
        # Fill rest
        for p in other_outers:
            lon, speed, retro = ep.get_planet_data(date, p)
            if lon is not None:
                row[f'{p}_Speed'] = speed
                
        # Retro count
        count = 0
        for p in ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']:
            # We don't have full retro flags here, let's approximate or fetch
            _, _, r = ep.get_planet_data(date, p)
            if r: count += 1
        row['retrograde_count'] = count
        
        # Predict
        # We need to ensure all cols exist, handle missing with 0
        for col in feature_cols:
            if col not in row: row[col] = 0
            
        X = pd.DataFrame([row])[feature_cols]
        risk = 1 - model.predict_proba(X)[0][1]
        
        print(f"{date.strftime('%Y-%m-%d'):<12} | {prob:>10.2f} | {risk:>8.2%}")
        results.append({'Date': date, 'Risk': risk, 'Flash': prob})
        
    # Save
    pd.DataFrame(results).to_csv('data/processed/final_audited_history.csv')

if __name__ == "__main__":
    audit_1987_daily()
