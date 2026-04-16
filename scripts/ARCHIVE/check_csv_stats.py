import pandas as pd
import numpy as np
import os
from pathlib import Path

def check_csv_stats():
    # PATH
    csv_path = r'd:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5\data\processed\refined_features.csv'
    df = pd.read_csv(csv_path)
    
    print(f"Total Rows: {len(df)}")
    print(f"Max SMI in CSV: {df['Sovereign_Malefic_Index'].max()}")
    
    # Ground Truth columns: Crash_20pct_6M, Crash_10pct_6M, Crash_5pct_6M
    # Signal triggers (Let's try SMI levels)
    for smi_thresh in [7.0, 8.0, 9.0]:
        print(f"\n--- TESTING SMI THRESHOLD: {smi_thresh} ---")
        alerts = df['Sovereign_Malefic_Index'] >= smi_thresh
        
        for tier in [5, 10, 20]:
            gt_col = f'Crash_{tier}pct_6M'
            if gt_col not in df.columns: continue
            
            tp = ((alerts == True) & (df[gt_col] == 1)).sum()
            fp = ((alerts == True) & (df[gt_col] == 0)).sum()
            fn = ((alerts == False) & (df[gt_col] == 1)).sum()
            tn = ((alerts == False) & (df[gt_col] == 0)).sum()
            
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            accuracy = (tp + tn) / (tp + tn + fp + fn)
            
            print(f"Tier -{tier}%: Recall={recall:.1%}, Precision={precision:.1%}, Accuracy={accuracy:.1%}, Signals={alerts.sum()}")

if __name__ == "__main__":
    check_csv_stats()
