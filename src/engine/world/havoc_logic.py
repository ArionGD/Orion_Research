from src.engine.astro.core.ephemeris_provider import EphemerisProvider
import itertools

class GlobalHavocLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        self.outer_planets = ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
        self.all_track = ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'True_Node']
        
    def calculate_havoc_features(self, date, prev_date=None):
        """
        Calculates the Cyclical Index (Barbault), Havoc metrics, Declination, and Nodes.
        Returns a dictionary of global features.
        """
        # 1. Get Positions and Declination
        positions = {}
        declinations = {}
        for p in self.all_track:
            lon, _, _, decl = self.ep.get_planet_data(date, p)
            if lon is not None:
                positions[p] = lon
                declinations[p] = decl
            else:
                if p != 'True_Node': # Basic outer planets are mandatory
                    return {} 
        
        # 2. Iterate 10 Pairs (Outer Planets only for Barbault)
        pairs = list(itertools.combinations(self.outer_planets, 2))
        
        total_distance = 0
        for p1_name, p2_name in pairs:
            dist = self.ep.get_distance(positions[p1_name], positions[p2_name])
            total_distance += dist
            
        # 3. Cyclical Index (Sum of distances)
        cyclical_index = total_distance
        
        # 4. Havoc Velocity (Change from previous)
        havoc_velocity = 0
        if prev_date:
            prev_total = 0
            has_prev_data = True
            for p1_name, p2_name in pairs:
                l1, _, _, _ = self.ep.get_planet_data(prev_date, p1_name)
                l2, _, _, _ = self.ep.get_planet_data(prev_date, p2_name)
                if l1 is None or l2 is None:
                    has_prev_data = False
                    break
                prev_dist = self.ep.get_distance(l1, l2)
                prev_total += prev_dist
                
            if has_prev_data:
                havoc_velocity = cyclical_index - prev_total
        
        # 5. Out of Bounds Check (> 23.5 deg)
        oob_count = 0
        for p, decl in declinations.items():
            if abs(decl) > 23.5:
                oob_count += 1
        
        # 6. Global Alert Level
        global_alert = 0
        for p in self.outer_planets: # World Point for outer planets
            lon = positions.get(p)
            if lon is not None:
                dist_to_WP = min(abs(lon - 0), abs(lon - 360))
                if dist_to_WP <= 1.0:
                    global_alert = 1
                    break
        
        # 7. Lunar Node Specifics (For Backtest Weighting)
        node_lon = positions.get('True_Node', 0)
        
        return {
            'Global_Stability_Index': cyclical_index,
            'Havoc_Velocity': havoc_velocity,
            'Havoc_Alert_Level': global_alert,
            'OOB_Count': oob_count,
            'True_Node_Lon': node_lon
        }
