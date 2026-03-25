from src.engine.astro.core.ephemeris_provider import EphemerisProvider

class SaturnConjunctions:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def analyze_neptune_relation(self, date, prev_date=None):
        """
        Returns a dictionary of Saturn-Neptune feature logic.
        MOVED FROM: src/engine/planets/saturn_neptune/logic.py
        """
        # Get Positions
        s_lon, s_speed, s_retro, _ = self.ep.get_planet_data(date, 'Saturn')
        n_lon, n_speed, n_retro, _ = self.ep.get_planet_data(date, 'Neptune')
        
        if s_lon is None or n_lon is None:
            return {}
            
        features = {}
        
        # 1. Individual Data (Optional, but useful for main table)
        features['Saturn_Lon'] = s_lon
        features['Neptune_Lon'] = n_lon
        features['Saturn_Speed'] = s_speed
        features['Neptune_Speed'] = n_speed
        features['Saturn_Retro'] = s_retro
        features['Neptune_Retro'] = n_retro
        
        # 2. Angle
        # Helper needed or calculate manually
        # E.g. self.ep.get_distance(s_lon, n_lon) - Does EP have this?
        # Checking EP code previously, it did not have get_distance visible in snippet.
        # Assuming simple math.
        angle = abs(s_lon - n_lon)
        if angle > 180: angle = 360 - angle
        
        features['Saturn_Neptune_Angle'] = angle
        
        # 3. Orb & Intensity
        orb = 8.0
        dist_0 = abs(angle - 0)
        dist_90 = abs(angle - 90)
        dist_180 = abs(angle - 180)
        min_dist = min(dist_0, dist_90, dist_180)
        
        features['is_hard_aspect'] = 1 if min_dist <= orb else 0
        features['aspect_intensity'] = max(0, 10 - min_dist)
        
        # 4. Convergence (Is Applying)
        if prev_date:
            s_prev, _, _, _ = self.ep.get_planet_data(prev_date, 'Saturn')
            n_prev, _, _, _ = self.ep.get_planet_data(prev_date, 'Neptune')
            
            if s_prev is not None:
                prev_angle = abs(s_prev - n_prev)
                if prev_angle > 180: prev_angle = 360 - prev_angle
                
                prev_min_dist = min(
                    abs(prev_angle - 0), abs(prev_angle - 90), abs(prev_angle - 180)
                )
                features['is_applying'] = 1 if min_dist < prev_min_dist else 0
            else:
                features['is_applying'] = 0
        else:
            features['is_applying'] = 0 # Default if no history
            
        return features
