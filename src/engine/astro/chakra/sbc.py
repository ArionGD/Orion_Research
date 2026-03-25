class SarvatobhadraChakra:
    """
    Sarvatobhadra Chakra (SBC) Logic
    81-Square Grid mapping Transits to Nakshatras/Sounds/Tithis
    """
    def __init__(self):
        # 28 Nakshatra System (Attributes Abhijit) for SBC
        self.nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu',
            'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta',
            'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha',
            'Uttara Ashadha', 'Abhijit', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
            'Uttara Bhadrapada', 'Revati'
        ]
        
    def get_vedha(self, planet_nak_idx, direction):
        """
        Calculate Vedha (Obstruction/Hit)
        Front, Left, Right Vedha based on SBC diagonal rules.
        """
        # Simplified Logic for Key Vedhas
        # Front Vedha is usually +14 Nakshatras (Opposition)
        # Left/Right depend on vowel/consonant type (complex).
        
        # For Arion V1 (Crash Detection):
        # We only care about "Cross Vedha" (X-pattern) on key stars.
        
        vedha_targets = []
        
        # Determine the "Cross" targets based on 28-star grid
        # Corner stars hit center. Center hits corners.
        # This requires a full grid coordinate system.
        
        # Placeholder for V1: Opposition is strong Vedha.
        opposition_idx = (planet_nak_idx + 14) % 28
        vedha_targets.append(self.nakshatras[opposition_idx])
        
        # Trine Vedha (Indices +9, +18 approx)
        trine_1 = (planet_nak_idx + 9) % 28
        trine_2 = (planet_nak_idx + 18) % 28
        vedha_targets.append(self.nakshatras[trine_1])
        vedha_targets.append(self.nakshatras[trine_2])
        
        return vedha_targets
        
    def check_crash_vedha(self, positions):
        """
        Check if Malefics (Saturn/Mars) are hitting Benefics (Jupiter/Venus)
        via Vedha.
        """
        score = 0
        signals = []
        
        # Get Nakshatra Indices (0-27)
        # 13 deg 20 min per nak generally, but Abhijit modifies this.
        # Simplified: Use 360 / 27 for mapping standard 27, then interpolate.
        
        # Let's use a standard mapper for V1
        
        malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu']
        benefics = ['Jupiter', 'Venus', 'Mercury', 'Moon']
        
        for m in malefics:
            if m not in positions: continue
            m_lon = positions[m]
            m_nak_idx = int(m_lon / 13.333333) % 27 
            # Note: Using 27 system for now as 28 is very complex to implement without ephemeris support
            
            # Check opposition (7th aspect is Vedha-like)
            opp_nak_idx = (m_nak_idx + 13) % 27
            
            for b in benefics:
                 if b not in positions: continue
                 b_lon = positions[b]
                 b_nak_idx = int(b_lon / 13.333333) % 27
                 
                 if b_nak_idx == opp_nak_idx:
                     score += 15 # Malefic hitting Benefic
                     signals.append(f"SBC Vedha: {m} hits {b}")
                     
        return score, signals
