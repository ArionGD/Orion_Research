class DeclinationLogic:
    """
    Handles '3D' Astrology: Declination and Out of Bounds (OOB) physics.
    """
    OOB_LIMIT = 23.44 # Earth's Axial Tilt limit
    
    def __init__(self):
        pass
        
    def is_out_of_bounds(self, declination):
        """
        Returns True if declination is beyond the Ecliptic limit.
        This indicates 'Wild' or 'Extreme' behavior.
        """
        if declination is None: return False
        return abs(declination) > self.OOB_LIMIT
        
    def get_oob_score(self, planet_name, declination):
        """
        Returns a Risk Multiplier based on OOB status.
        """
        if not self.is_out_of_bounds(declination):
            return 1.0
            
        # OOB Logic
        # Mars OOB -> Extreme Aggression/Volatility
        # Venus OOB -> Extreme Value Deviations (Bubbles/Crashes)
        # Moon OOB -> Extreme Sentiment
        
        multiplier = 1.0
        
        if planet_name == 'Mars':
            multiplier = 1.5 # The "Wild Fire" Multiplier
        elif planet_name == 'Venus':
            multiplier = 1.25 # The "Bubble" Multiplier
        elif planet_name == 'Moon':
            multiplier = 1.1 # Sentiment swing
            
        return multiplier
