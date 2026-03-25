from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility
import swisseph as swe

class TemporalScanner:
    """
    Scans for time-based Medini events: Eclipses, Ingress (Sankranti), Stations.
    """
    
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def set_sidereal_mode(self, mode=swe.SIDM_LAHIRI):
        self.ep.set_sidereal_mode(mode)
        
    def get_angular_separation(self, lon1, lon2):
        """Minimal separation on the circle (0-180)."""
        diff = abs(lon1 - lon2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def check_eclipse_potential(self, date):
        """
        Checks if a date has Eclipse potential (Syzygy + Node proximity).
        Returns: None or dict with Eclipse details.
        """
        # 1. Get Positions
        sun, _, _, _ = self.ep.get_planet_data(date, 'Sun')
        moon, _, _, _ = self.ep.get_planet_data(date, 'Moon')
        rahu, _, _, _ = self.ep.get_planet_data(date, 'True_Node')
        
        if None in [sun, moon, rahu]: return None
        
        ketu = (rahu + 180) % 360
        
        # 2. Check Syzygy (New Moon or Full Moon)
        sun_moon_dist = self.get_angular_separation(sun, moon)
        
        is_new_moon = sun_moon_dist < 15 # Wide orb for "Season"
        is_full_moon = abs(sun_moon_dist - 180) < 15
        
        if not (is_new_moon or is_full_moon):
            return None
            
        # 3. Check Node Proximity (Eclipse Limit ~18 degrees)
        # Check Sun distance to Rahu or Ketu
        dist_sun_rahu = self.get_angular_separation(sun, rahu)
        dist_sun_ketu = self.get_angular_separation(sun, ketu)
        
        min_node_dist = min(dist_sun_rahu, dist_sun_ketu)
        
        if min_node_dist < 18.0:
            e_type = "Solar" if is_new_moon else "Lunar"
            intensity = "Partial"
            if min_node_dist < 10.0: intensity = "Total/Annular" # Simplified
            if min_node_dist < 1.5: intensity = "Exact Central"
            
            return {
                'Type': f"{intensity} {e_type} Eclipse",
                'Node_Distance': round(min_node_dist, 2),
                'Axis': f"{ZodiacUtility.get_rasi(rahu)[0]}/{ZodiacUtility.get_rasi(ketu)[0]}"
            }
            
        return None

    def check_ingress(self, planet, date1, date2):
        """
        Checks if a planet changed Sign (Rasi) between date1 and date2.
        Sankranti usually refers to Sun, but applies to all.
        """
        lon1, _, _, _ = self.ep.get_planet_data(date1, planet)
        lon2, _, _, _ = self.ep.get_planet_data(date2, planet)
        
        if lon1 is None or lon2 is None: return None
        
        rasi1, _, _ = ZodiacUtility.get_rasi(lon1)
        rasi2, _, _ = ZodiacUtility.get_rasi(lon2)
        
        if rasi1 != rasi2:
            return {
                'Event': f"{planet} Ingress (Sankranti)",
                'From': rasi1,
                'To': rasi2
            }
        return None

    def scan_temporal_events(self, date):
        """
        Snapshot scan for single date events (Eclipse).
        """
        events = []
        eclipse = self.check_eclipse_potential(date)
        if eclipse:
            events.append(eclipse)
        return events
