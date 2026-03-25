"""
Arion.ai Defensive & Commodity Modifier
=======================================
Detects structural safe-haven flight during a macro crisis.
Differentiates between 'Risk-Off' (Sell Tech/Banks) and 'Safe-Haven' (Buy Gold/Pharma).

Astro-Logic for Commodities:
1. GOLD (Sun / Jupiter): Rises when Saturn (Fear) aspects Sun or Jupiter is exalted/stationary.
2. SILVER (Moon / Venus): Industrial metal masquerading as precious. Fails during true deflationary crashes unless Venus is exalted.
3. PHARMA/HEALTHCARE (Sun / Ketu): Outperforms during Rahu/Ketu nodal returns (Biological shocks).
4. CONSUMER STAPLES (Moon / Cancer): The absolute safety net.
"""

from src.engine.astro.core.zodiac import ZodiacUtility

class DefensiveModifier:
    def __init__(self):
        self.safe_havens = ['Gold', 'Pharma', 'Staples']
        self.fake_havens = ['Silver'] # Proven by backtest to crash with equities
        
    def check_safe_havens(self, transit_positions, havoc_score):
        """
        Determines if the crash signature supports a rotation into Gold or Pharma.
        """
        suggestions = {
            'Technology': 'SHORT',
            'Discretionary': 'SHORT',
            'Financials': 'SHORT',
            'Gold': 'HOLD/BUY',
            'Silver': 'SHORT',  # Astrologically Moon-ruled, but acts industrial
            'Pharma': 'HOLD',
            'Staples': 'HOLD'
        }
        
        # If no severe crash, normal rules apply
        if havoc_score < 35:
             return {"Rotation": "Normal Market Metrics Apply", "Tiers": None}
             
        # Astrological Triggers for GOLD super-spike
        sun_pos = transit_positions.get('Sun', 0)
        saturn_pos = transit_positions.get('Saturn', 0)
        jupiter_pos = transit_positions.get('Jupiter', 0)
        rahu_pos = transit_positions.get('True_Node', 0)
        
        # 1. Gold Super-Cycle: Saturn aspecting Sun or Jupiter
        # Usually creates supreme Fear (Saturn) restricting Value (Jupiter/Sun). Flight to literal Gold.
        dist_sat_sun = min(abs(saturn_pos - sun_pos), 360 - abs(saturn_pos - sun_pos))
        if dist_sat_sun < 10 or abs(dist_sat_sun - 180) < 10 or abs(dist_sat_sun - 90) < 10:
             suggestions['Gold'] = 'STRONG BUY (Fear Premium)'
             
        # 2. Pharma/Healthcare Spike: Nodal axis involved (Rahu/Ketu)
        # Ketu brings viruses/obscure illness. Rahu brings global panic over it.
        # If Nodal axis is active (e.g., Eclipse season or Rahu stationary)
        # Checked via Rahu position relative to World Axis (0 Aries/Libra)
        if min(abs(rahu_pos - 0), abs(rahu_pos - 180)) < 15:
             suggestions['Pharma'] = 'STRONG BUY (Biological/Nodal Panic)'
             
        # 3. Silver Warning: Fails as a hedge
        # Despite being a precious metal, Moon's volatility means it crashes with panic.
        suggestions['Silver'] = 'SHORT (Industrial/Panic Vulnerable)'
        
        return suggestions
