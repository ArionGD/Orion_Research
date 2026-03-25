from src.engine.astro.core.ephemeris_provider import EphemerisProvider

class SolarEclipseLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def check_eclipse(self, date):
        """
        Checks for Solar Eclipse conditions.
        Condition: New Moon (Sun-Moon < 1 deg) AND Proximity to Rahu/Ketu (< 18 deg).
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
        
        # 1. New Moon Check
        sun_moon_sep = abs(sun - moon)
        if sun_moon_sep > 180: sun_moon_sep = 360 - sun_moon_sep
        
        if sun_moon_sep > 13.0: # Widen to ~1 day (Moon moves ~12-13 deg/day)
            return {'Is_Eclipse': False, 'Score': 0}
            
        # 2. Node Proximity
        dist_rahu = abs(sun - rahu)
        if dist_rahu > 180: dist_rahu = 360 - dist_rahu
        
        dist_ketu = abs(sun - ketu)
        if dist_ketu > 180: dist_ketu = 360 - dist_ketu
        
        min_node_dist = min(dist_rahu, dist_ketu)
        
        # Eclipse Limits (Approx)
        # Total: < 9 deg
        # Partial: < 18 deg
        
        if min_node_dist > 18.0:
             return {'Is_Eclipse': False, 'Score': 0}
             
        eclipse_type = "Partial"
        score = 5 # Base impact
        
        if min_node_dist < 9.0:
            eclipse_type = "Total/Annular"
            score = 10
            
        if min_node_dist < 2.0:
             eclipse_type = "Exact Central"
             score = 15
             
        return {
            'Is_Eclipse': True,
            'Type': f"{eclipse_type} Solar Eclipse",
            'Dist_Node': round(min_node_dist, 2),
            'Score': score
        }
