class NakshatraMapper:
    """
    Handles conversion of Longitude to Nakshatra and Koorma Directions.
    """
    def __init__(self):
        self.nakshatras = [
            {"name": "Ashwini", "ruler": "Ketu"},           # 0
            {"name": "Bharani", "ruler": "Venus"},          # 1
            {"name": "Krittika", "ruler": "Sun"},           # 2
            {"name": "Rohini", "ruler": "Moon"},            # 3
            {"name": "Mrigashira", "ruler": "Mars"},        # 4
            {"name": "Ardra", "ruler": "Rahu"},             # 5
            {"name": "Punarvasu", "ruler": "Jupiter"},      # 6
            {"name": "Pushya", "ruler": "Saturn"},          # 7
            {"name": "Ashlesha", "ruler": "Mercury"},       # 8
            {"name": "Magha", "ruler": "Ketu"},             # 9
            {"name": "Purva Phalguni", "ruler": "Venus"},   # 10
            {"name": "Uttara Phalguni", "ruler": "Sun"},    # 11
            {"name": "Hasta", "ruler": "Moon"},             # 12
            {"name": "Chitra", "ruler": "Mars"},            # 13
            {"name": "Swati", "ruler": "Rahu"},             # 14
            {"name": "Vishakha", "ruler": "Jupiter"},       # 15
            {"name": "Anuradha", "ruler": "Saturn"},        # 16
            {"name": "Jyeshtha", "ruler": "Mercury"},       # 17
            {"name": "Mula", "ruler": "Ketu"},              # 18
            {"name": "Purva Ashadha", "ruler": "Venus"},    # 19
            {"name": "Uttara Ashadha", "ruler": "Sun"},     # 20
            {"name": "Shravana", "ruler": "Moon"},          # 21
            {"name": "Dhanishta", "ruler": "Mars"},         # 22
            {"name": "Shatabhisha", "ruler": "Rahu"},       # 23
            {"name": "Purva Bhadrapada", "ruler": "Jupiter"},# 24
            {"name": "Uttara Bhadrapada", "ruler": "Saturn"},# 25
            {"name": "Revati", "ruler": "Mercury"}          # 26
        ]
        
        # Koorma Chakra Mapping (Nakshatras mapped to Directions)
        # 3 Stars per direction usually.
        # User defined: Rohini, Mrigashira, Ardra = Center.
        # Standard: Krittika, Rohini, Mrig.
        # Let's align around user request for Center.
        # Center: Rohini(3), Mrig(4), Ardra(5).
        # We need to map the rest sequentially or by standard?
        # Standard Koorma is specific.
        # Let's use a standard mapping but overriding Center as requested if different.
        # Standard (Varahamihira):
        # Center: Krittika(2), Rohini(3), Mrig(4)
        # East: Ardra(5), Punarvasu(6), Pushya(7)
        # SE: Ashlesha(8), Magha(9), P.Phal(10)
        # South: U.Phal(11), Hasta(12), Chitra(13)
        # SW: Swati(14), Vishakha(15), Anuradha(16)
        # West: Jyeshtha(17), Mula(18), P.Ash(19)
        # NW: U.Ash(20), Shravana(21), Dhan(22)
        # North: Shat(23), P.Bhad(24), U.Bhad(25)
        # NE: Revati(26), Ashwini(0), Bharani(1)
        
        # User requested: Rohini, Mrigashira, Ardra = Center.
        # This shifts the wheel by 1 star. I will facilitate the User Request.
        
        self.koorma_map = {
            "Center": ["Rohini", "Mrigashira", "Ardra"], # 3, 4, 5
            "East": ["Punarvasu", "Pushya", "Ashlesha"], # 6, 7, 8
            "South-East": ["Magha", "Purva Phalguni", "Uttara Phalguni"], # 9, 10, 11
            "South": ["Hasta", "Chitra", "Swati"], # 12, 13, 14
            "South-West": ["Vishakha", "Anuradha", "Jyeshtha"], # 15, 16, 17
            "West": ["Mula", "Purva Ashadha", "Uttara Ashadha"], # 18, 19, 20
            "North-West": ["Shravana", "Dhanishta", "Shatabhisha"], # 21, 22, 23
            "North": ["Purva Bhadrapada", "Uttara Bhadrapada", "Revati"], # 24, 25, 26
            "North-East": ["Ashwini", "Bharani", "Krittika"] # 0, 1, 2
        }
        
    def get_nakshatra(self, longitude):
        """
        Input: Longitude (0-360)
        Returns: {name, number, pada, ruler, direction}
        """
        if longitude is None: return None
        
        longitude = longitude % 360
        nak_len = 13.333333333 # 13 deg 20 min
        nak_idx = int(longitude / nak_len)
        
        # Details
        data = self.nakshatras[nak_idx]
        name = data['name']
        ruler = data['ruler']
        
        # Pada
        start_lon = nak_idx * nak_len
        remainder = longitude - start_lon
        pada_len = 3.333333333 # 3 deg 20 min
        pada = int(remainder / pada_len) + 1
        
        # Direction
        direction = "Unknown"
        for dir_name, stars in self.koorma_map.items():
            if name in stars:
                direction = dir_name
                break
                
        return {
            "name": name,
            "number": nak_idx + 1,
            "pada": pada,
            "ruler": ruler,
            "direction": direction
        }
