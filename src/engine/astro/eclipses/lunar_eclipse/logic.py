from src.engine.astro.core.ephemeris_provider import EphemerisProvider

class LunarEclipseLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def check_eclipse(self, date):
        """
        Checks for Lunar Eclipse conditions.
        Condition: Full Moon (Sun-Moon ~ 180 deg) AND Proximity to Rahu/Ketu (< 12 deg).
        Returns: {Is_Eclipse, Type, Score}
        """
        # Get Positions
        positions = self.ep.get_all_positions(date)
        if not positions:
            return {'Is_Eclipse': False, 'Score': 0}
            
        sun = positions['Sun']
        moon = positions['Moon']
        rahu = positions['True_Node']
        ketu = (rahu + 180) % 360
        
        # Full Moon Check (Sun-Moon ~ 180)
        sun_moon_sep = abs(sun - moon)
        dist_from_180 = abs(180 - sun_moon_sep)
        
        if dist_from_180 > 13.0: # Widen to ~1 day
            return {'Is_Eclipse': False, 'Score': 0}
            
        # 2. Node Proximity (Moon to Node)
        # For Lunar Eclipse, Moon must be near Node.
        dist_rahu = abs(moon - rahu)
        if dist_rahu > 180: dist_rahu = 360 - dist_rahu
        
        dist_ketu = abs(moon - ketu)
        if dist_ketu > 180: dist_ketu = 360 - dist_ketu
        
        min_node_dist = min(dist_rahu, dist_ketu)
        
        # Eclipse Limits (Lunar is tighter than Solar)
        # Total: < 9 deg
        # Partial: < 12 deg
        
        if min_node_dist > 13.0:
             return {'Is_Eclipse': False, 'Score': 0}
             
        eclipse_type = "Partial"
        score = 4 # Lunar eclipse is slightly less "Structural" than Solar, but affects sentiment
        
        if min_node_dist < 9.0:
            eclipse_type = "Total/Annular"
            score = 8
            
        return {
            'Is_Eclipse': True,
            'Type': f"{eclipse_type} Lunar Eclipse",
            'Dist_Node': round(min_node_dist, 2),
            'Score': score
        }
