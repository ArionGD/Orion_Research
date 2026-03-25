import pandas as pd
import numpy as np
import yfinance as yf
import os
from scipy.stats import pearsonr
from datetime import datetime, timedelta
from src.engine.world.havoc_logic import GlobalHavocLogic

class BacktestEngine:
    def __init__(self):
        self.logic = GlobalHavocLogic()
        self.node_weight = 1.0
        
    def get_vix_data(self, start="1990-01-01", end="2025-01-01"):
        print(f"Fetching VIX data from {start} to {end}...")
        vix = yf.download("^VIX", start=start, end=end)
        # Handle multi-index if yfinance returns it
        if isinstance(vix.columns, pd.MultiIndex):
            vix.columns = vix.columns.get_level_values(0)
        return vix[['Close']].rename(columns={'Close': 'VIX'})

    def calculate_havoc_series(self, dates, node_weight):
        scores = []
        for date in dates:
            prev_date = date - timedelta(days=1)
            feats = self.logic.calculate_havoc_features(date, prev_date)
            
            if not feats:
                scores.append(np.nan)
                continue
            
            # Composite Havoc Score
            # 1. Normalized Stability Index (Inverse)
            # Stability index usually ranges from 500 to 1500? No, sum of 10 pairs (0-180 each).
            # Max = 1800, Min = 0.
            gsi = feats.get('Global_Stability_Index', 900)
            norm_gsi = (1800 - gsi) / 1800.0 # High when index is low (Compression)
            
            # 2. OOB Impact
            oob = feats.get('OOB_Count', 0)
            oob_impact = oob / 5.0
            
            # 4. Havoc Velocity (The "Shock" factor)
            velocity = abs(feats.get('Havoc_Velocity', 0))
            norm_velocity = min(1.0, velocity / 50.0) # Relative to typical move
            
            # 3. Node Activity (Proximity to 0 Aries or 0 Libra - the World Axis)
            node_lon = feats.get('True_Node_Lon', 0)
            node_dist = min(abs(node_lon - 0), abs(node_lon - 180), abs(node_lon - 360))
            node_impact = max(0, (5 - node_dist) / 5.0) if node_dist < 5 else 0
            
            # Weighted Score
            total_score = (norm_gsi * 0.3) + (norm_velocity * 0.5) + (oob_impact * 0.1) + (node_impact * node_weight)
            scores.append(total_score)
            
        return pd.Series(scores, index=dates)

    def run_backtest(self):
        vix_df = self.get_vix_data()
        dates = vix_df.index
        
        print("Calculating Arion Havoc Scores...")
        vix_monthly = vix_df.resample('M').mean() # Resample to avoid daily noise
        
        best_corr = -1
        best_weight = self.node_weight
        
        # Test weights for Lunar Node
        weights_to_test = [0.1, 0.5, 1.0, 2.0, 3.0, 5.0]
        
        for w in weights_to_test:
            scores = self.calculate_havoc_series(vix_monthly.index, w)
            combined = pd.DataFrame({'VIX': vix_monthly['VIX'], 'Havoc': scores}).dropna()
            
            corr, _ = pearsonr(combined['VIX'], combined['Havoc'])
            print(f"Weight {w}: Correlation = {corr:.4f}")
            
            if corr > best_corr:
                best_corr = corr
                best_weight = w
                
        print(f"\nFinal Result: Best Correlation = {best_corr:.4f} with Node Weight = {best_weight}")
        
        if best_corr < 0.6:
            print("ALERT: Correlation below 0.6 goal. Optimization required.")
        else:
            print("SUCCESS: Correlation meets target threshold.")
            
        return best_weight, best_corr

if __name__ == "__main__":
    engine = BacktestEngine()
    engine.run_backtest()
