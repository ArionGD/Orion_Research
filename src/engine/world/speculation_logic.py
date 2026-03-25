from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from datetime import timedelta

class SpeculationLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def calculate_speculation_features(self, date):
        """
        Calculates features related to financial speculation and flash crashes.
        Focus: Venus-Uranus cycle.
        Scans the upcoming month (date to date+30) to catch fleeting events.
        """
        max_prob = 0.0
        max_angle = 0.0
        is_hard_flash_found = 0
        is_uranus_stat_found = 0
        
        # Scan 5-day intervals to save time, or every 3 days. 
        # Venus moves ~1 deg/day. A 3-degree orb lasts ~6 days.
        # Scanning every 5 days ensures we hit the window.
        # Better: Scan every 3 days.
        for i in range(0, 31, 3):
            scan_date = date + timedelta(days=i)
            
            # Get Data at scan point
            v_lon, v_speed, v_retro, _ = self.ep.get_planet_data(scan_date, 'Venus')
            u_lon, u_speed, u_retro, _ = self.ep.get_planet_data(scan_date, 'Uranus')
            
            if v_lon is None or u_lon is None:
                continue
                
            # 1. Venus-Uranus Angle
            angle = self.ep.get_distance(v_lon, u_lon)
            
            # 2. Aspect Checks
            # Major Hard Aspects (0, 90, 180) - Orb 3.0
            dist_0 = abs(angle - 0)
            dist_90 = abs(angle - 90)
            dist_180 = abs(angle - 180)
            is_major_hard = 1 if min(dist_0, dist_90, dist_180) <= 3.0 else 0
            
            # Minor Hard Aspects (45, 135) - Orb 2.0 (8th Harmonic)
            dist_45 = abs(angle - 45)
            dist_135 = abs(angle - 135)
            # Check 8th harmonic: 45 and 135.
            is_minor_hard = 1 if min(dist_45, dist_135) <= 2.0 else 0
            
            current_is_hard = 1 if (is_major_hard or is_minor_hard) else 0
            
            # 3. Uranus Stationery Check
            current_is_stat = 1 if abs(u_speed) < 0.02 else 0
            
            # 4. Score
            raw_score = 0
            if is_major_hard:
                raw_score += 0.5
            elif is_minor_hard:
                raw_score += 0.4 
                
            if current_is_stat:
                raw_score += 0.4
                if current_is_hard:
                    raw_score += 0.1
            
            prob = min(1.0, raw_score)
            
            if prob > max_prob:
                max_prob = prob
                max_angle = angle # snapshot angle at peak risk
            
            if current_is_hard: is_hard_flash_found = 1
            if current_is_stat: is_uranus_stat_found = 1
            
        return {
            'Venus_Uranus_Angle': max_angle,
            'Flash_Crash_Probability': max_prob,
            'is_hard_flash': is_hard_flash_found,
            'is_uranus_stationary': is_uranus_stat_found
        }
