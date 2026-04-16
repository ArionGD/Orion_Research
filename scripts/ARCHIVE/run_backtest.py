import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

def run_benchmark():
    print("Initializing Arion.ai Historical Benchmark Audit...")

    # Load Data and Model
    data_path = 'data/processed/refined_features.csv'
    model_path = 'models/arion_v2.joblib'
    
    if not os.path.exists(data_path) or not os.path.exists(model_path):
        print("Error: Missing data or model files.")
        return
        
    df = pd.read_csv(data_path, parse_dates=['Date'], index_col='Date')
    model = joblib.load(model_path)
    
    # Target Events (Approximate windows)
    # Using specific dates requested, but ensuring they exist in monthly index
    # Note: Our data is monthly start 'MS' or last price based on yfinance.
    # We will look for Month-Start approximation.
    events = {
        'Great Crash (1929)': '1929-10-01',
        'WWII Start (1939)': '1939-09-01',
        'Oil Crisis (1973)': '1973-10-01',
        'Black Monday (1987)': '1987-10-01',
        'Lehman/GFC (2008)': '2008-09-01',
        'COVID Crash (2020)': '2020-03-01'
    }
    
    # Check if dates exist in DF (normalize to 1st of month just in case)
    valid_events = {}
    for name, date_str in events.items():
        dt = pd.Timestamp(date_str)
        # Find nearest index if not exact match (though our dataset is monthly)
        idx = df.index.get_indexer([dt], method='nearest')[0]
        actual_date = df.index[idx]
        
        # Ensure it's the same year/month
        if actual_date.year == dt.year and actual_date.month == dt.month:
            valid_events[name] = actual_date
        else:
            print(f"Warning: Exact data for {name} ({date_str}) not found. Nearest: {actual_date}")
            valid_events[name] = actual_date # Use nearest for robustness
    
    # Prepare Feature Set for Prediction
    # Must match training feature_cols EXACTLY:
    # ['Saturn_Neptune_Angle' 'is_hard_aspect' 'aspect_intensity' 'is_applying'
    # 'retrograde_count' 'Global_Stability_Index' 'Havoc_Velocity'
    # 'Havoc_Alert_Level' 'Mars_Volatility_Score' 'Saturn_Speed'
    # 'Neptune_Speed' 'Mars_Speed' 'Jupiter_Speed' 'Uranus_Speed' 'Pluto_Speed']
    
    feature_cols = [
        'Saturn_Neptune_Angle', 'is_hard_aspect', 'aspect_intensity', 'is_applying', 
        'retrograde_count', 'Global_Stability_Index', 'Havoc_Velocity', 
        'Havoc_Alert_Level', 'OOB_Count', 'True_Node_Lon', 'Mars_Volatility_Score', 
        'Flash_Crash_Probability', 'is_uranus_stationary', 'is_hard_flash',
        'Saturn_Speed', 'Neptune_Speed', 'Mars_Speed', 
        'Jupiter_Speed', 'Uranus_Speed', 'Pluto_Speed'
    ]
         
    print("\n" + "="*80)
    print(f"{'EVENT NAME':<20} | {'DATE':<10} | {'GSI':<8} | {'Havoc':<5} | {'Mars':<4} | {'Flash':<5} | {'Risk':<6}")
    print("="*80)
    
    results = []
    
    for name, date_idx in valid_events.items():
        row = df.loc[date_idx]
        
        # Predict
        X_input = row[feature_cols].values.reshape(1, -1)
        X_df = pd.DataFrame(X_input, columns=feature_cols).astype(float) # Ensure float dtypes for XGB
        
        # Prob of Bullish
        prob_bull = model.predict_proba(X_df)[0][1]
        havoc_score = 1 - prob_bull
        
        gsi = row['Global_Stability_Index']
        vel = row['Havoc_Velocity']
        mars = row['Mars_Volatility_Score']
        flash = row['Flash_Crash_Probability']
        
        print(f"{name:<20} | {date_idx.strftime('%Y-%m'):<10} | {gsi:>8.2f} | {vel:>5.2f} | {mars:>4.2f} | {flash:>5.2f} | {havoc_score:>6.2%}")
        
        results.append({
            'Event': name,
            'Havoc_Score': havoc_score
        })
        
    print("-" * 80)
    
    # Visualization
    res_df = pd.DataFrame(results)
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(res_df['Event'], res_df['Havoc_Score'], color='crimson', alpha=0.8)
    
    plt.axhline(0.65, color='black', linestyle='--', alpha=0.5, label='Risk Threshold (0.65)')
    
    plt.title('Arion.ai Historical Audit: Event Stress Signatures', fontsize=14)
    plt.ylabel('Havoc Score (Probability of Bearish/Crash)')
    plt.xticks(rotation=45)
    plt.ylim(0, 1.0)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add values
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1%}', ha='center', va='bottom')
                 
    plt.tight_layout()
    output_path = 'data/processed/benchmark_audit.png'
    plt.savefig(output_path)
    print(f"\nBenchmark visualization saved to: {output_path}")

if __name__ == "__main__":
    run_benchmark()
