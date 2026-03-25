import swisseph as swe
import os

class EphemerisProvider:
    """
    Universal provider for planetary positions using Swiss Ephemeris.
    """
    def __init__(self, ephe_path=None):
        if ephe_path and os.path.exists(ephe_path):
            swe.set_ephe_path(ephe_path)
            
        # Map Planet Names to SwissEph IDs
        self.planet_ids = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN,
            'Uranus': swe.URANUS, 
            'Neptune': swe.NEPTUNE,
            'Pluto': swe.PLUTO,
            'True_Node': swe.TRUE_NODE,
            'Chiron': swe.CHIRON if hasattr(swe, 'CHIRON') else (swe.AST_OFFSET + 2060),
            'Lilith': 21 # 21 is typically Mean Apogee in SE. If not, try swe.MEAN_APOG
        }
        self.is_sidereal = False
    
    def get_julian_day(self, date):
        """Calculates Julian Day for 12:00 UTC."""
        return swe.julday(date.year, date.month, date.day, 12.0)
    
    def get_planet_data(self, date, planet_name):
        """
        Returns (longitude, speed, is_retrograde, declination) for a specific planet.
        """
        if planet_name == 'Ketu':
             # Special case for Ketu
             rahu_lon, _, _, _ = self.get_planet_data(date, 'True_Node')
             if rahu_lon is None: return None, None, None, None
             ketu_lon = self.get_ketu_position(rahu_lon)
             return ketu_lon, 0, 0, 0 # Ketu roughly mirrors Rahu speed/decl but simpler to return pos only first

        jd = self.get_julian_day(date)
        if planet_name not in self.planet_ids:
            raise ValueError(f"Unknown planet: {planet_name}")
            
        pid = self.planet_ids[planet_name]
        flags = swe.FLG_SPEED | swe.FLG_SWIEPH
        if self.is_sidereal:
            flags |= swe.FLG_SIDEREAL
        
        try:
            # Ecliptic coordinates for longitude and speed
            res, _ = swe.calc_ut(jd, pid, flags)
            lon = res[0]
            speed = res[3]
            is_retro = 1 if speed < 0 else 0
            
            # Equatorial coordinates for declination (Standard usually tropical for declination, 
            # but for consistency we use same flags or strip Sidereal? 
            # Declination is usually measured from Equator, Sidereal affects ZODIACAL longitude.
            # We will keep flags consistent for now, but declination is physical.)
            res_equ, _ = swe.calc_ut(jd, pid, flags | swe.FLG_EQUATORIAL)
            decl = res_equ[1]
            
            return lon, speed, is_retro, decl
        except swe.Error:
            try:
                # Fallback to Moshier
                res, _ = swe.calc_ut(jd, pid, swe.FLG_SPEED | swe.FLG_MOSEPH)
                lon = res[0]
                speed = res[3]
                is_retro = 1 if speed < 0 else 0
                
                res_equ, _ = swe.calc_ut(jd, pid, swe.FLG_SPEED | swe.FLG_MOSEPH | swe.FLG_EQUATORIAL)
                decl = res_equ[1]
                
                return lon, speed, is_retro, decl
            except:
                return None, None, None, None

    def get_distance(self, lon1, lon2):
        """Calculates internal angular distance (0-180)."""
        diff = abs(lon1 - lon2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def set_sidereal_mode(self, ayanamsa=swe.SIDM_LAHIRI):
        """Sets the calculation mode to Sidereal (Vedic)."""
        swe.set_sid_mode(ayanamsa)
        self.is_sidereal = True

    def get_ketu_position(self, rahu_lon):
        """Calculates Ketu (South Node) from Rahu (True Node)."""
        if rahu_lon is None: return None
        return (rahu_lon + 180) % 360

    def get_all_positions(self, date):
        """
        Returns a dictionary of all planetary longitudes for the given date.
        Useful for modules that need the full sky (e.g., Eclipses, Yogas).
        """
        positions = {}
        for p in self.planet_ids.keys():
            lon, _, _, _ = self.get_planet_data(date, p)
            if lon is not None:
                positions[p] = lon
                
        if 'True_Node' in positions:
            positions['Ketu'] = (positions['True_Node'] + 180) % 360
            
        return positions
        
    def get_declination(self, date, planet_name):
        """
        Returns the declination (latitude relative to Equator) of a planet.
        Used for Out of Bounds (OOB) checks.
        """
        _, _, _, decl = self.get_planet_data(date, planet_name)
        return decl

    def get_true_nodes(self, date):
        """
        Returns dictionary with 'Rahu' (True Node) and 'Ketu' positions.
        """
        rahu_lon, _, _, _ = self.get_planet_data(date, 'True_Node')
        if rahu_lon is None:
            return {'Rahu': None, 'Ketu': None}
            
        ketu_lon = self.get_ketu_position(rahu_lon)
        return {'Rahu': rahu_lon, 'Ketu': ketu_lon}
        
    def get_houses(self, date, lat, lon):
        """
        Calculates Ascendant (Lagna) and MC (10th Cusp).
        Returns: { 'Ascendant': deg, 'MC': deg, 'Houses': [deg, ...] }
        """
        jd = self.get_julian_day(date)
        
        # Calculate Houses (Placidus is default Western, but for Vedic we often use Whole Sign or Porphyry.
        # However, Ascendant point is same regardless of system).
        # 'P' for Placidus, 'W' for Whole Sign. We need the Ascendant degree primarily.
        
        cusps, ascmc = swe.houses(jd, lat, lon, b'P') 
        
        return {
            'Ascendant': ascmc[0],
            'MC': ascmc[1],
            'Armc': ascmc[2],
            'Vertex': ascmc[3]
        }

    def get_sunrise_sunset(self, date, lat, lon):
        """
        Returns (sunrise_jd, sunset_jd) for the given date/location.
        """
        jd = self.get_julian_day(date)
        
        # swe.rise_trans returns: (status, rise_jd, set_jd, transit_jd...)
        # We look for SUN (0)
        # Ephe flag: swe.FLG_SWIEPH
        # We need to target the sunrise of the CURRENT day.
        
        # We need to target the sunrise of the CURRENT day.
        
        # res returns tuple. Index 1 = Rise time (JD)
        try:
            # Try without starname (some bindings omit it for planets?)
            res = swe.rise_trans(jd, swe.SUN, swe.FLG_SWIEPH, lon, lat, 0)
        except TypeError:
            # Try with original 0 string for starname but check if planet ID works
            try:
                # Some docs say: swe.rise_trans(jd, planet, starname, flags...)
                # If swe.SUN is 0, maybe explicitly using int 0 for starname helps?
                res = swe.rise_trans(jd, swe.SUN, 0, swe.FLG_SWIEPH, lon, lat, 0)
            except:
                return None, None
        
        if res[0] != 0: # Check status
             return None, None
             
        rise_jd = res[1][0]
        set_jd = res[1][1]
        
        return rise_jd, set_jd

    def get_fixed_star(self, star_name, date):
        """
        Returns (longitude, None, None, None) for a fixed star.
        """
        jd = self.get_julian_day(date)
        flags = swe.FLG_SWIEPH
        if self.is_sidereal:
             flags |= swe.FLG_SIDEREAL
             
        try:
            # star_name e.g., ",Algol" (comma important for search?)
            # or just "Algol"
            # return: (name, [lon, lat, dist, ...], error)
            res = swe.fixstar_ut(star_name, jd, flags)
            # res is ((name), (lon, lat...), 'error')
            lon = res[1][0]
            return lon, 0, 0, 0
        except:
            return None, None, None, 0
