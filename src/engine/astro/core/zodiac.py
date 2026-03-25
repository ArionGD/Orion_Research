class ZodiacUtility:
    """
    Utility for converting longitudes to Vedic Zodiac (Rasi) and Nakshatras.
    """
    
    RASIS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 
        'Leo', 'Virgo', 'Libra', 'Scorpio', 
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta',
        'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    @staticmethod
    def get_rasi(longitude):
        """
        Returns (Sign Name, Index 0-11, Degrees within Sign).
        """
        norm_lon = longitude % 360
        idx = int(norm_lon // 30)
        degrees = norm_lon % 30
        return ZodiacUtility.RASIS[idx], idx, degrees

    @staticmethod
    def get_nakshatra(longitude):
        """
        Returns (Nakshatra Name, Index 0-26, Pada 1-4).
        One Nakshatra = 13 degrees 20 minutes = 13.3333... degrees.
        One Pada = 3 degrees 20 minutes = 3.3333... degrees.
        """
        norm_lon = longitude % 360
        
        # Nakshatra Index
        nak_span = 360 / 27 # 13.3333
        nak_idx = int(norm_lon // nak_span)
        
        # Degrees traversed in current nakshatra
        rem_deg = norm_lon % nak_span
        
        # Pada (Quarter)
        pada_span = nak_span / 4 # 3.3333
        pada = int(rem_deg // pada_span) + 1
        
        return ZodiacUtility.NAKSHATRAS[nak_idx], nak_idx, pada

    @staticmethod
    def get_dms_str(deg):
        d = int(deg)
        m = int((deg - d) * 60)
        s = int(((deg - d) * 60 - m) * 60)
        return f"{d}°{m}'{s}\""
