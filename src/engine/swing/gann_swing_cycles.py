import pandas as pd
from datetime import datetime, timedelta

class SwingCycleAssaultRifle:
    """
    Arion.ai Tier 3: SWING TRADING ASSAULT RIFLE
    ============================================
    This engine predicts Medium-Term market drops (3 to 6-week down cycles).
    It answers the question: 'Which month and which week will the market drop?'
    
    Logic: Gann's 'Square of 52' and Natural Vibration Cycles.
    Major trends reverse exactly:
    - 30 days (1 month), 60 days, 90 days, 180 days after a major peak/bottom.
    - Specifically, the 45th and 90th days are lethal shorting zones.
    If multiple vibration counts overlap on the same calendar week, that week 
    is mathematically flagged for a 'Swing Drop'.
    """
    
    def __init__(self):
        # Gann's most dangerous vibration numbers (in Calendar Days)
        self.lethal_cycles = [30, 45, 60, 90, 120, 135, 180, 270, 360]
        self.lookback_days = 365
        
    def find_historical_peaks(self, daily_df: pd.DataFrame, top_n: int = 3) -> dict:
        """
        Scans the past year of daily S&P500/Nifty data to find the absolute
        Major Peaks and Bottoms. These act as the 'Seed Vibrations'.
        """
        # Ensure data is sorted
        daily_df = daily_df.sort_index()
        
        # We need significant peaks/troughs. A simple 20-day local max/min finder.
        daily_df['Local_Max'] = daily_df['High'] == daily_df['High'].rolling(20, center=True).max()
        daily_df['Local_Min'] = daily_df['Low'] == daily_df['Low'].rolling(20, center=True).min()
        
        sig_peaks = daily_df[daily_df['Local_Max']].index.tolist()
        sig_bottoms = daily_df[daily_df['Local_Min']].index.tolist()
        
        return {
            'Peaks': sig_peaks[-top_n:] if len(sig_peaks) >= top_n else sig_peaks,
            'Bottoms': sig_bottoms[-top_n:] if len(sig_bottoms) >= top_n else sig_bottoms
        }
        
    def generate_annual_swing_calendar(self, daily_df: pd.DataFrame, target_year: int) -> pd.DataFrame:
        """
        Generates the 'Swing Drop/Rally Calendar' for the specified year.
        Calculates distinct directionality:
        - X days from a PEAK -> The market has been falling and is due to BOTTOM (Buy Signal).
        - X days from a BOTTOM -> The market has been rallying and is due to TOP OUT (Short Signal).
        """
        seeds = self.find_historical_peaks(daily_df, top_n=5)
        
        target_start = datetime(target_year, 1, 1)
        target_end = datetime(target_year, 12, 31)
        
        threat_days = []
        
        # 1. Calculate from Major Peaks (Forms Bottoms -> BULLISH / BUY)
        for peak_date in seeds['Peaks']:
            for cycle in self.lethal_cycles:
                hit_date = peak_date + timedelta(days=cycle)
                if target_start <= hit_date <= target_end:
                    weight = 2 if cycle in [45, 90, 180] else 1
                    threat_days.append({
                        'Date': hit_date,
                        'Cycle_Type': f"{cycle}d-from-Peak",
                        'Direction': 'BULLISH (Buy Dip)',
                        'Score': weight  # Positive for Bullish
                    })
                    
        # 2. Calculate from Major Bottoms (Forms Peaks -> BEARISH / SHORT)
        for bottom_date in seeds['Bottoms']:
            for cycle in self.lethal_cycles:
                hit_date = bottom_date + timedelta(days=cycle)
                if target_start <= hit_date <= target_end:
                    weight = 2 if cycle in [45, 90, 180] else 1
                    threat_days.append({
                        'Date': hit_date,
                        'Cycle_Type': f"{cycle}d-from-Bottom",
                        'Direction': 'BEARISH (Short Top)',
                        'Score': -weight # Negative for Bearish
                    })
                    
        threat_df = pd.DataFrame(threat_days)
        if threat_df.empty:
            return pd.DataFrame()
            
        threat_df['Week_Number'] = threat_df['Date'].dt.isocalendar().week
        threat_df['Month'] = threat_df['Date'].dt.strftime('%B')
        
        # Aggregate the weekly net sentiment
        weekly_risk = threat_df.groupby(['Month', 'Week_Number']).agg(
            Total_Hits=('Date', 'count'),
            Net_Direction_Score=('Score', 'sum'),
            Overlapping_Cycles=('Cycle_Type', lambda x: list(x))
        ).reset_index()
        
        # Determine the ultimate explicit bias for that week
        def get_bias(score):
            if score >= 3: return 'STRONG BUY (Max Bottom Geometry)'
            elif score > 0: return 'LEAN BULLISH (Swing Long)'
            elif score <= -3: return 'STRONG SHORT (Max Exhaustion Geometry)'
            elif score < 0: return 'LEAN BEARISH (Swing Short)'
            return 'NEUTRAL (Choppy/Mixed Signals)'
            
        weekly_risk['Trade_Action'] = weekly_risk['Net_Direction_Score'].apply(get_bias)
        
        # Sort by the absolute intensity of the geometry (most explosive weeks first)
        weekly_risk['Intensity'] = weekly_risk['Net_Direction_Score'].abs()
        weekly_risk = weekly_risk.sort_values(by='Intensity', ascending=False).drop(columns=['Intensity'])
        
        return weekly_risk

# Example Usage:
# df = yf.download('^NSEI', start='2025-01-01', end='2026-03-01')
# assault_rifle = SwingCycleAssaultRifle()
# calendar = assault_rifle.generate_annual_swing_calendar(df, 2026)
