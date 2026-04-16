import pandas as pd
import numpy as np
import swisseph as swe
import joblib
import os
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Import functions from existing modules if possible, 
# but for standalone robustness, we'll re-implement the core astro logic here
# or we could import from src.data.ingestor and src.features if they were refactored into importable modules.
# Given previous context, src/features.py and src/ingestor.py were scripts. 
# We'll inline the necessary logic for the cleanest execution.

def get_future_planet_positions(date):
    """
    Calculates geocentric longitude and speed for outer planets using swisseph.
    """
    # Calculate Julian Day for 12:00 UTC
    jd = swe.julday(date.year, date.month, date.day, 12.0)
    
    planets = {
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS, 
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO,
        'Mars': swe.MARS
    }
    
    features = {}
    flags = swe.FLG_SPEED | swe.FLG_SWIEPH 
    
    for name, pid in planets.items():
        try:
            res, _ = swe.calc_ut(jd, pid, flags)
            lon = res[0]
            speed = res[3]
            
            features[f'{name}_Lon'] = lon
            features[f'{name}_Speed'] = speed
            # Retrograde flag
            features[f'{name}_Retro'] = 1 if speed < 0 else 0
            
        except swe.Error as e:
             # Fallback
             try:
                 res, _ = swe.calc_ut(jd, pid, swe.FLG_SPEED | swe.FLG_MOSEPH)
                 lon = res[0]
                 speed = res[3]
                 features[f'{name}_Lon'] = lon
                 features[f'{name}_Speed'] = speed
                 features[f'{name}_Retro'] = 1 if speed < 0 else 0
             except:
                 return None

    # Calculate Saturn-Neptune Angle
    if 'Saturn_Lon' in features and 'Neptune_Lon' in features:
        diff = abs(features['Saturn_Lon'] - features['Neptune_Lon'])
        if diff > 180:
            diff = 360 - diff
        features['Saturn_Neptune_Angle'] = diff
    
    return features

def generate_prophecy():
    print("Generating Arion.ai Prophecy Report (2026-2030)...")

    # 1. Model Loading
    model_path = 'models/arion_v2.joblib'
    if not os.path.exists(model_path):
        print("Error: Model not found.")
        return
    model = joblib.load(model_path)
    
    # 2. Data Generation (Feb 2026 to Dec 2030)
    # Target current March 2026 too for audit.
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2030, 12, 1)
    
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += relativedelta(months=1)
        
    print(f"Generating features for {len(dates)} future months...")
    
    astro_data = []
    for d in dates:
        row = get_future_planet_positions(d)
        if row:
            astro_data.append(row)
        else:
             # Should not happen with built-in ephe
             pass
             
    df = pd.DataFrame(astro_data, index=dates)
    df.index.name = 'Date'

    # 3. Feature Engineering (Match training logic)
    print("Applying Orb & Intensity Logic...")
    
    # a. Orb Logic
    angle_col = 'Saturn_Neptune_Angle'
    orb = 8.0
    
    dist_0 = abs(df[angle_col] - 0)
    dist_90 = abs(df[angle_col] - 90)
    dist_180 = abs(df[angle_col] - 180)
    min_dist = pd.concat([dist_0, dist_90, dist_180], axis=1).min(axis=1)
    
    df['is_hard_aspect'] = (min_dist <= orb).astype(int)
    df['aspect_intensity'] = (10 - min_dist).clip(lower=0)
    
    # b. Convergence (is_applying)
    df['dist_to_exact'] = min_dist
    df['is_applying'] = (df['dist_to_exact'] < df['dist_to_exact'].shift(1)).astype(int)
    # Fill first month applying based on assumption or previous known data (here 0 for safety)
    df['is_applying'] = df['is_applying'].fillna(0)
    
    # c. Retrograde Count
    retro_cols = [c for c in df.columns if 'Retro' in c]
    df['retrograde_count'] = df[retro_cols].sum(axis=1)

    # d. Structural/Derived Mocking for Future (Need to assume defaults for non-astro)
    df['Global_Stability_Index'] = 650 # Default middle-ground
    df['Havoc_Velocity'] = 0.5
    df['Havoc_Alert_Level'] = 0
    df['OOB_Count'] = 1
    df['True_Node_Lon'] = 180 # Arbitrary node middle
    df['Mars_Volatility_Score'] = 0.0
    df['Flash_Crash_Probability'] = 0.4
    df['is_uranus_stationary'] = 0
    df['is_hard_flash'] = 0

    # 4. Prediction
    # MUST MATCH XGBOOST TRAINED ORDER
    feature_cols = [
        'Saturn_Neptune_Angle', 'is_hard_aspect', 'aspect_intensity', 'is_applying', 
        'retrograde_count', 'Global_Stability_Index', 'Havoc_Velocity', 
        'Havoc_Alert_Level', 'OOB_Count', 'True_Node_Lon', 'Mars_Volatility_Score', 
        'Flash_Crash_Probability', 'is_uranus_stationary', 'is_hard_flash',
        'Saturn_Speed', 'Neptune_Speed', 'Mars_Speed', 
        'Jupiter_Speed', 'Uranus_Speed', 'Pluto_Speed'
    ]
    
    X_future = df[feature_cols]
    
    # predict_proba returns [prob_class_0, prob_class_1]
    # Class 1 = Bullish
    probs = model.predict_proba(X_future)
    bullish_prob = probs[:, 1]
    
    df['Bullish_Probability'] = bullish_prob
    df['Havoc_Score'] = 1 - bullish_prob

    # 5. Save Output
    output_dir = 'data/processed'
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'prophecy_2026_2030.csv')
    df.to_csv(out_file)
    print(f"Prophecy saved to: {out_file}")

    # 6. Visualization
    plt.figure(figsize=(12, 6))
    
    plt.plot(df.index, df['Havoc_Score'], color='crimson', linewidth=2, label='Havoc Score (Risk)')
    
    # Highlight high risk zones
    high_risk = df[df['Havoc_Score'] > 0.65]
    plt.scatter(high_risk.index, high_risk['Havoc_Score'], color='black', zorder=5, label='Extreme Risk (>65%)')
    
    for date, score in high_risk['Havoc_Score'].items():
        plt.annotate(f"{date.strftime('%Y-%m')}", 
                     (date, score), 
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center',
                     fontsize=8,
                     color='darkred')
    
    plt.axhline(0.65, color='gray', linestyle='--', alpha=0.5)
    plt.title('Arion.ai Prophecy: Mundane Risk Timeline (2026-2030)', fontsize=14)
    plt.ylabel('Havoc Score (1 - Bullish Prob)')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    viz_path = os.path.join(output_dir, 'prophecy_timeline.png')
    plt.savefig(viz_path)
    print(f"Visualization saved to: {viz_path}")
    
    # Print high risk dates
    if not high_risk.empty:
        print("\nWARNING: High Havoc Scores Detected on:")
        print(high_risk[['Havoc_Score', 'Saturn_Neptune_Angle']].sort_values('Havoc_Score', ascending=False))

if __name__ == "__main__":
    generate_prophecy()
