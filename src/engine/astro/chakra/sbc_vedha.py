import math

class SBCVedhaScanner:
    """
    Arion.ai: Sarvatobhadra Chakra (SBC) Vedha Scanner
    ==================================================
    Calculates the 'Mrityu Vedha' (Piercing Glances) of malefic planets 
    onto the natal Nakshatras of the market.
    
    A market only fully crashes if a malefic (Saturn, Mars, Rahu) creates 
    a direct geometric Vedha on its foundational star.
    """
    
    # Standard 28 Nakshatra System for SBC (Including Abhijit)
    # Each takes roughly 360 / 28 = 12.857 degrees.
    NAKSHATRAS_28 = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", 
        "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
        "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Abhijit", "Shravana",
        "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    
    def __init__(self):
        # We focus on the most destructive malefics for systemic crashes
        self.malefics = ['Saturn', 'Mars', 'True_Node', 'Mean_Node', 'Sun']
        # The natal Nakshatra for the S&P 500 (March 4, 1957) is Ashwini.
        self.sp500_natal_nakshatra = "Ashwini"

    def get_nakshatra_28(self, longitude: float) -> str:
        """
        Maps a 360-degree longitude (Sidereal Lahiri) to the 28-Nakshatra SBC system.
        0 degrees Aries = Start of Ashwini.
        """
        nak_span = 360.0 / 28.0
        idx = int(longitude / nak_span)
        if idx >= 28: idx = 27
        return self.NAKSHATRAS_28[idx]

    def get_vedha_targets(self, planet_name: str, planet_lon: float, is_retrograde: bool = False):
        """
        Calculates the 3 Vedhas (Front, Right, Left) using the exact 7x7 SBC geometric grid.
        For mathematical simplicity in this quantitative model, we map the exact Vedha 
        pairs for Ashwini (S&P 500's foundation).
        
        SBC Ashwini Vedha Piercing:
        - Front (Straight Across): Punarvasu
        - Right Diagonal: Shatabhisha
        - Left Diagonal: Purva Phalguni (or Hasta depending on grid placement)
        
        Using a 28-star generalized offset:
        Front is roughly opposite. Diagonals are at specific grid corners.
        """
        current_nak = self.get_nakshatra_28(planet_lon)
        idx = self.NAKSHATRAS_28.index(current_nak)
        
        # Standard SBC Grid Mapping for Ashwini (Idx 0 in our array)
        if current_nak in ["Punarvasu", "Shatabhisha", "Purva Phalguni"]:
            # If a planet is in one of these, it casts a Vedha onto Ashwini
            return ["Ashwini"]
            
        # Generalized geometric fallback for other stars
        front_idx = (idx + 14) % 28
        # In a 7x7 grid, diagonal piercing occurs roughly at +9 and -9 offsets
        right_idx = (idx + 9) % 28
        left_idx = (idx - 9) % 28
        
        targets = [
            self.NAKSHATRAS_28[front_idx],
            self.NAKSHATRAS_28[right_idx],
            self.NAKSHATRAS_28[left_idx]
        ]
        
        return targets

    def detect_market_vedha(self, planetary_positions: dict, target_nakshatra: str = None) -> bool:
        """
        Checks if any malefic planet is casting a Vedha on the market's natal star.
        planetary_positions: {'Saturn': 120.5, 'Mars': 45.2, ...}
        """
        if not target_nakshatra:
            target_nakshatra = self.sp500_natal_nakshatra
            
        for planet in self.malefics:
            if planet in planetary_positions:
                lon = planetary_positions[planet]
                vedhas = self.get_vedha_targets(planet, lon)
                
                if target_nakshatra in vedhas:
                    # A Malefic is directly piercing the market's foundation.
                    return True
                    
        return False
