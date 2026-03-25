from .profile import USACountryProfile

class USARiskEngine:
    def __init__(self):
        self.profile = USACountryProfile()
        self.natal = self.profile.get_sensitive_points()
        
    def check_risk(self, transit_positions):
        """
        Compares transit positions to USA Natal Chart.
        Returns score, signals.
        """
        score = 0
        signals = []
        
        t_saturn = transit_positions.get('Saturn')
        t_mars = transit_positions.get('Mars')
        t_rahu = transit_positions.get('True_Node')
        
        n_moon = self.natal['Moon'] # US Moon (Aquarius ~27)
        n_sun = self.natal['Sun']   # US Sun (Gemini ~22)
        n_saturn = self.natal['Saturn']
        
        # 1. Sade Sati (Saturn conjunct Moon)
        if t_saturn and n_moon:
            diff = abs(t_saturn - n_moon)
            if diff > 180: diff = 360 - diff
            if diff < 10.0: # Wide orb for Sade Sati Peak
                score += 15
                signals.append("USA: Sade Sati Peak (Saturn on Moon)")
                
        # 2. Saturn on Natal Sun (Authority Crisis)
        if t_saturn and n_sun:
            diff = abs(t_saturn - n_sun)
            if diff > 180: diff = 360 - diff
            if diff < 5.0:
                score += 20
                signals.append("USA: Saturn crushed Authority (on Sun)")
                
        # 3. Mars on Natal Rahu (Violence)
        n_rahu = self.natal['Rahu']
        if t_mars and n_rahu:
            diff = abs(t_mars - n_rahu)
            if diff > 180: diff = 360 - diff
            if diff < 3.0:
                score += 10
                signals.append("USA: Mars triggers Rahu (Violence/panic)")
                
        # 4. Saturn Return (Cyclical Crisis)
        if t_saturn and n_saturn:
            diff = abs(t_saturn - n_saturn)
            if diff > 180: diff = 360 - diff
            if diff < 3.0:
                score += 10
                signals.append("USA: Saturn Return (Structural Reset)")
        
        # 5. Jupiter Transits (Expansion/Transformation)
        t_jupiter = transit_positions.get('Jupiter')
        if t_jupiter:
            # Jupiter on Natal Rahu (US 8th House - Strategic Financial Transformation)
            n_rahu = self.natal['Rahu']
            if n_rahu:
                diff = abs(t_jupiter - n_rahu)
                if diff > 180: diff = 360 - diff
                if diff < 5.0:
                    score -= 8 # Strong positive offset for strategic deals
                    signals.append("USA: Jupiter on Natal Rahu (Global Strategic Deal/Wealth Transformation)")

            # Jupiter in Cancer (US 8th House)
            if 90 < t_jupiter < 120:
                score -= 2
                signals.append("USA: Jupiter in 8th (International Debt/Trade Re-alignment)")

        return score, signals
