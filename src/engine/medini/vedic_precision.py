import numpy as np

class VedicHighPrecisionEngine:
    """
    Advanced Vedic Structural Layers:
    1. Ashtakavarga (Sign Strength / Bindus)
    2. Varga Proxy (Navamsha Debilitation check)
    3. Sandhi Pulse (Planetary transition zones)
    """
    
    # 2026 Example Bindu Strengths (To be derived from Natal Chart)
    # NIFTY Signs (Cancer Moon): Strength of signs based on Ashtakavarga
    # Standard: 28 pts is 'Average'. Below 20 is 'Extreme Fragility'. 
    # Above 32 is 'Stone Wall'.
    INDIA_ASHTAKAVARGA = {
        'Aries': 24, 'Taurus': 30, 'Gemini': 28, 'Cancer': 34, # Birth Moon
        'Leo': 20, 'Virgo': 22, 'Libra': 26, 'Scorpio': 18,   # Fragile Signs
        'Sagittarius': 34, 'Capricorn': 28, 'Aquarius': 24, 'Pisces': 26
    }
    
    US_ASHTAKAVARGA = {
        'Aries': 28, 'Taurus': 26, 'Gemini': 34, 'Cancer': 28,
        'Leo': 24, 'Virgo': 30, 'Libra': 22, 'Scorpio': 20,
        'Sagittarius': 28, 'Capricorn': 34, 'Aquarius': 26, 'Pisces': 24
    }

    RASIS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 
        'Leo', 'Virgo', 'Libra', 'Scorpio', 
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]

    def get_sign_multiplier(self, planet_lon, market='INDIA'):
        """
        Calculates the 'Fragility Multiplier' based on Sign Strength (Bindus).
        If strength < 25, the drop is amplified.
        """
        idx = int((planet_lon % 360) // 30)
        sign = self.RASIS[idx]
        
        strength_map = self.INDIA_ASHTAKAVARGA if market == 'INDIA' else self.US_ASHTAKAVARGA
        strength = strength_map.get(sign, 28)
        
        # Multiplier Logic:
        # Strength 34 -> 0.7x (Dampener)
        # Strength 28 -> 1.0x (Neutral)
        # Strength 18 -> 1.8x (Amplifier of Chaos)
        multiplier = 1.0 + (28 - strength) * 0.05 
        return max(0.5, multiplier), strength

    def get_sandhi_pulse(self, planet_lon):
        """
        Planetary Sandhi (Transition Zones).
        Crashes are triggered when planets are at 0-2 degrees or 28-30 degrees of a sign.
        'Sandhi' means the planet is 'Old' or 'Infant' - unstable.
        """
        deg_in_sign = planet_lon % 30
        if deg_in_sign <= 2.0 or deg_in_sign >= 28.0:
            return 1.5 # 50% increase in volatility pulse
        return 1.0

    def get_varga_debility(self, planet_lon):
        """
        Navamsha (D9) Debility Proxy.
        Calculates if the planet falls into a debilitated sign in Navamsha.
        """
        # A simple mathematical proxy for D9 sign:
        # Each Navamsha is 3 deg 20 min. 9 Navamshas per sign.
        nav_idx = int((planet_lon % 360) // (3.333333))
        # This idx maps to a specific sign in Navamsha chart
        # We check if this Navamsha sign is the planet's sign of fall (Nicha).
        # Example: Mars is Nicha in Cancer (Sign 3).
        return 1.2 if (nav_idx % 12 == 3) else 1.0
