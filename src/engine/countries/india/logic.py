
import math

class IndiaRiskEngine:
    """
    India (Republic/Independence) Logic
    Natal Chart: August 15, 1947, 00:00 IST, Delhi
    Lagna: Taurus (Vrishabha) ~8 degrees
    Moon: Cancer (Pushya Nakshatra)
    """
    def __init__(self):
        # Degrees 0-360
        self.natal_positions = {
            'Sun': 117.85, # Cancer (Ashlesha)
            'Moon': 100.15, # Cancer (Pushya) - Mind of Nation
            'Mars': 86.85, # Gemini (Ardra)
            'Mercury': 103.50, # Cancer (Pushya)
            'Jupiter': 205.50, # Libra (Vishakha)
            'Venus': 102.50, # Cancer (Pushya)
            'Saturn': 110.45, # Cancer (Ashlesha)
            'Rahu': 35.30, # Taurus (Krittika)
            'Ketu': 215.30, # Scorpio (Anuradha)
            'Lagna': 38.50 # Taurus (Rohini)
        }
        
    def check_risk(self, current_positions):
        """
        Check transits against India's Natal Chart.
        Returns: (Risk Score, List of Signals)
        """
        score = 0
        signals = []
        
        # 1. Sade Sati (Saturn over Natal Moon)
        # Natal Moon is in Cancer (90-120)
        # Sade Sati happens when Saturn is in Gemini (60-90), Cancer (90-120), Leo (120-150).
        sat_pos = current_positions.get('Saturn', 0)
        
        # 12th from Moon (Gemini)
        if 60 <= sat_pos < 90:
            score += 15
            signals.append("India: Sade Sati Rising (Stress)")
        # Over Moon (Cancer) - PEAK
        elif 90 <= sat_pos < 120:
            score += 25
            signals.append("India: Sade Sati Peak (Crisis)")
        # 2nd from Moon (Leo)
        elif 120 <= sat_pos < 150:
            score += 10
            signals.append("India: Sade Sati Setting (Residual Stress)")
            
        # 2. Saturn Transit to 10th House (Aquarius) -> Government/Economy stress
        # Lagna is Taurus. 10th from Taurus is Aquarius (300-330).
        if 300 <= sat_pos < 330:
            score += 10
            signals.append("India: Saturn in 10th (Governance Stress)")
            
        # 3. Mars over Natal Rahu (Taurus) -> Communal/Border Tension
        # Natal Rahu is ~35 deg (Taurus).
        mar_pos = current_positions.get('Mars', 0)
        if abs(mar_pos - self.natal_positions['Rahu']) < 5:
            score += 20
            signals.append("India: Mars Conjunct Natal Rahu (Explosive Tension)")
        
        # 4. Jupiter protection
        # Jupiter over Natal Moon is great (Gajakesari Transit).
        jup_pos = current_positions.get('Jupiter', 0)
        # Check aspect or conjunction. Trine (120 deg) is good too.
        # Conjunction check
        if abs(jup_pos - self.natal_positions['Moon']) < 10:
             score -= 10 # Reduces risk
             signals.append("India: Jupiter Blessing (Protection)")
             
        return score, signals
