class VargaCalculator:
    """
    Divisional Charts (Vargas) Calculator
    Standard Parashara Formatting
    """
    def __init__(self):
        self.zodiac = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 
            'Leo', 'Virgo', 'Libra', 'Scorpio', 
            'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
    def get_sign_from_lon(self, lon):
        idx = int(lon / 30) % 12
        return self.zodiac[idx]
        
    def calculate_d9(self, lon):
        """
        Navamsa (D9)
        Each Sign (30 deg) is divided into 9 parts (3deg 20min each).
        Formula: (Lon * 9) % 360
        """
        d9_lon = (lon * 9) % 360
        # However, traditional calculation is sign-based.
        # This mathematical shortcut gives the correct sign position.
        return self.get_sign_from_lon(d9_lon)
        
    def calculate_d10(self, lon):
        """
        Dasamsa (D10) - Career / Status
        Formula: 
        1. Determine if Sign is Odd or Even.
        2. If Odd: Count from Sign itself.
        3. If Even: Count from 9th from Sign.
        """
        sign_idx = int(lon / 30) % 12
        deg_in_sign = lon % 30
        part = int(deg_in_sign / 3.0) # 10 parts of 3 degrees
        
        # Odd Signs: Aries(0), Gemini(2), Leo(4), Libra(6), Sag(8), Aq(10)
        is_odd = (sign_idx % 2 == 0) # 0-indexed, so 0=Aries (Odd)
        
        if is_odd:
            # Count from Sign itself
            target_sign_idx = (sign_idx + part) % 12
        else:
            # Count from 9th from Sign
            ninth_idx = (sign_idx + 8) % 12
            target_sign_idx = (ninth_idx + part) % 12
            
        return self.zodiac[target_sign_idx]
        
    def get_varga_strength(self, planet, d1_lon):
        """
        Check Varga Bala (Strength)
        Simple Check: Is it Vargottama? (Same sign in D1 and D9)
        """
        d1_sign = self.get_sign_from_lon(d1_lon)
        d9_sign = self.calculate_d9(d1_lon)
        
        is_vargottama = (d1_sign == d9_sign)
        return {
            'D1': d1_sign,
            'D9': d9_sign,
            'D10': self.calculate_d10(d1_lon),
            'Is_Vargottama': is_vargottama
        }
