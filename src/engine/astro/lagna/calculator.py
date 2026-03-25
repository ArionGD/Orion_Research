from src.engine.astro.core.ephemeris_provider import EphemerisProvider
import swisseph as swe

class LagnaCalculator:
    def __init__(self):
        self.ep = EphemerisProvider()
        
        # Standard Rasi Lords (0=Aries...11=Pisces)
        self.rasi_lords = {
            0: 'Mars',    # Aries
            1: 'Venus',   # Taurus
            2: 'Mercury', # Gemini
            3: 'Moon',    # Cancer
            4: 'Sun',     # Leo
            5: 'Mercury', # Virgo
            6: 'Venus',   # Libra
            7: 'Mars',    # Scorpio
            8: 'Jupiter', # Sagittarius
            9: 'Saturn',  # Capricorn
            10: 'Saturn', # Aquarius
            11: 'Jupiter' # Pisces
        }
    
    def get_zodiac_sign(self, lon):
        return int(lon // 30)

    def calculate_special_lagnas(self, date, lat, lon):
        """
        Calculates Ascendant, MC, HL, GL, and AL.
        Returns dictionary of longitudes.
        """
        # 1. Physical Lagnas (Ascendant / MC)
        houses = self.ep.get_houses(date, lat, lon)
        asc_deg = houses['Ascendant']
        mc_deg = houses['MC']
        
        # 2. Sunrise Logic for HL/GL
        rise_jd, _ = self.ep.get_sunrise_sunset(date, lat, lon)
        if rise_jd is None:
            # Fallback (e.g., polar latitudes or error)
            rise_jd = self.ep.get_julian_day(date) - 0.25 # Approx 6am
            
        current_jd = self.ep.get_julian_day(date)
        
        # Time elapsed in Days
        dt_days = current_jd - rise_jd
        if dt_days < 0:
             # Sunrise hasn't happened yet today (Pre-dawn), use previous sunrise? 
             # Or definition: Time from *Sunrise*. If pre-dawn, strict Vedic day starts at Sunrise.
             # For calculation simplicity, we assume we are looking at the relevant Vedic day. 
             # If dt_days is negative, it means we are before sunrise.
             # In Jaimini, we usually count from sunrise of the *current calendar day* or previous if night.
             # Lets treat negative as 0 for now or assume day-time market hours.
             dt_days = 0 
        
        # Time in Hours
        dt_hours = dt_days * 24.0
        
        # 3. Hora Lagna (HL)
        # Speed: 1 Sign (30 deg) per Hora (1 Hour approx / 2.5 Ghatis)
        # Formula: Sun_Lon_At_Sunrise + (Hours_Elapsed * 30)
        # Note: Some traditions use Ascendant as base. Standard BPHS uses Sunrise Sun.
        # Let's use Sunrise Sun + rate.
        
        sun_pos_rise_lon, _, _, _ = self.ep.get_planet_data(date, 'Sun') # Using current Sun is close enough to rise Sun
        
        # Actually HL = Sunrise Sun + (Time_Hours * 30)
        # But we need to handle wrapping 360
        
        hl_deg = (sun_pos_rise_lon + (dt_hours * 30)) % 360
        
        # 4. Ghatika Lagna (GL)
        # Speed: 1 Sign (30 deg) per Ghati (24 mins = 0.4 Hours)
        # Rate: 30 deg / 0.4 h = 75 deg per hour.
        
        gl_deg = (sun_pos_rise_lon + (dt_hours * 75)) % 360
        
        # 5. Arudha Lagna (AL)
        # Logic: Find Lord of Ascendant. 
        # Find position of Lord.
        # Measure distance (Houses) from Asc to Lord.
        # Project same distance forward from Lord.
        
        asc_sign = self.get_zodiac_sign(asc_deg)
        lord_name = self.rasi_lords[asc_sign]
        
        # Get Lord's position
        lord_lon, _, _, _ = self.ep.get_planet_data(date, lord_name)
        lord_sign = self.get_zodiac_sign(lord_lon)
        
        # Distance (Count inclusive, e.g. Aries to Aries = 1)
        # But math difference: Lord - Asc
        dist_signs = (lord_sign - asc_sign) % 12
        if dist_signs == 0: dist_signs = 12 # Same sign
        
        # Simple Arudha (No exceptions yet)
        # AL Sign = Lord Sign + Distance
        al_sign_idx = (lord_sign + dist_signs) % 12
        
        # Convert back to approx longitude (center of sign) for visualization
        al_deg = (al_sign_idx * 30) + 15
        
        return {
            'Ascendant': asc_deg,
            'MC': mc_deg,
            'Hora_Lagna': hl_deg,
            'Ghatika_Lagna': gl_deg,
            'Arudha_Lagna_Sign': al_sign_idx, # 0-11
            'Arudha_Lagna_Deg': al_deg,
            'Lagna_Lord': lord_name
        }
