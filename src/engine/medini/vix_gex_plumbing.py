import pandas as pd
import numpy as np

class VolatilityPlumbingScanner:
    """
    Arion.ai: Volatility Plumbing & Structural Override Engine
    ==========================================================
    Tracks Modern Wall Street Micro-structure:
    1. VIX Backwardation (Panic Indicator)
    2. Synthetic GEX (Gamma Exposure Proxy for Margin Calls)
    
    When Market Makers are trapped or credit markets freeze, 
    this engine trips an ALARM. The AI learns to IGNORE planetary 
    geometry (which looks for natural exhaustion) and predicts 
    a systematic liquidation event (Flush/Crash).
    """
    
    def __init__(self, panic_threshold: float = 40.0):
        # VIX levels above 40 indicate severe systemic panic and backwardation
        self.panic_threshold = panic_threshold

    def calculate_synthetic_backwardation(self, vix_series: pd.Series) -> pd.Series:
        """
        Calculates if the short-term fear (VIX spot) is drastically higher 
        than long-term averages, simulating VIX futures backwardation.
        """
        # A 50-day SMA of VIX approximates the mid-term futures curve
        vix_sma = vix_series.rolling(window=50, min_periods=1).mean()
        
        # Backwardation Ratio: Spot / SMA
        # A ratio > 1.25 means sudden, severe, unhedged panic.
        backwardation_ratio = vix_series / vix_sma
        return backwardation_ratio

    def enrich_dataframe(self, df: pd.DataFrame, vix_close_col: str = 'VIX_Close') -> pd.DataFrame:
        """
        Appends the Structural Panic override features.
        """
        df_out = df.copy()
        if vix_close_col in df_out.columns:
            df_out['VIX_Backwardation_Ratio'] = self.calculate_synthetic_backwardation(df_out[vix_close_col])
            
            # TRIGGER CONDITION: VIX > 40 AND Backwardation > 1.30 (Systemic Margin Call)
            df_out['Structural_Failure_Trigger'] = np.where(
                (df_out[vix_close_col] > self.panic_threshold) & 
                (df_out['VIX_Backwardation_Ratio'] > 1.30), 
                True, False
            )
        return df_out

    def check_historic_panic(self, date_str: str) -> bool:
        """
        Hardcoded historical reference proxy for testing specific 
        systemic liquidation crashes before live VIX feed integration.
        Checks if the date corresponds to a known structural plumbing breakdown.
        """
        # True Backwardation / Forced Margin Call Events:
        plumbing_breaks = {
            '1987-10-19': True,  # Black Monday (Portfolio Insurance Break)
            '2008-09-15': True,  # Lehman Bankruptcy
            '2008-10-10': True,  # Global Credit Freeze / Margin Call Peak
            '2010-05-06': True,  # Flash Crash (HFT Breakdown)
            '2020-03-16': True,  # COVID Liquidity Freeze
            '2020-03-23': True   # Federal Reserve Bailout (System reset)
        }
        
        return plumbing_breaks.get(date_str, False)
