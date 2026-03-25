import pandas as pd
import numpy as np
import joblib
import os

def find_ace_whipsaw():
    print("=== ACE: Arion Crash Engine - Forensic Whipsaw Audit (2000-2024) ===")
    
    # 1. Load Data & Model
    file_path = 'data/processed/refined_features.csv'
    if not os.path.exists(file_path):
        print("Error: Features not found.")
        return
        
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    # Filter for the test period (Last 15 years typically)
    df_test = df[df.index >= '2010-01-01']
    
    model = joblib.load('models/arion_v2_crash_predator.joblib')
    config = joblib.load('models/arion_v2_crash_predator_config.joblib')
    features = config['features']
    threshold = config['threshold']
    
    # Encode for Prediction
    df_test_encoded = pd.get_dummies(df_test, columns=['Mahadasha', 'Antardasha'])
    # Ensure columns match
    for col in features:
        if col not in df_test_encoded.columns:
            df_test_encoded[col] = 0
            
    X = df_test_encoded[features]
    y_true = df_test['Crash_20pct_6M']
    
    # Generate Predictions
    probs = model.predict_proba(X)[:, 1]
    y_pred = (probs >= threshold).astype(int)
    
    df_test['Prediction'] = y_pred
    df_test['Probability'] = probs
    
    # Find Whipsaws (False Positives: Pred=1, True=0)
    whipsaws = df_test[(df_test['Prediction'] == 1) & (df_test['Crash_20pct_6M'] == 0)]
    
    print("\n" + "="*60)
    print("ACE FORENSIC: IDENTIFIED WHIPSAWS (FALSE ALARMS)")
    print("="*60)
    
    if whipsaws.empty:
        print("No False Alarms detected in the recent test set. 100% Precision attained.")
    else:
        print(f"Total False Alarms: {len(whipsaws)}")
        print(whipsaws[['Probability', 'Sovereign_Malefic_Index', 'Saturn_Neptune_Angle']].head(10))
        
    # Also find Successful Hits
    hits = df_test[(df_test['Prediction'] == 1) & (df_test['Crash_20pct_6M'] == 1)]
    print("\n" + "="*60)
    print("ACE FORENSIC: SUCCESSFUL HITS (ACCURATE SHORTS)")
    print("="*60)
    print(hits[['Probability', 'Sovereign_Malefic_Index', 'Crash_20pct_6M']].head(10))

if __name__ == "__main__":
    find_ace_whipsaw()
