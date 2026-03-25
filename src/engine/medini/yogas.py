from src.engine.astro.core.ephemeris_provider import EphemerisProvider
import itertools

class YogaScanner:
    """
    Scans for Medini Jyotish Yogas (Planetary Combinations).
    Focus: Conjunctions (Yuti) and Planetary War (Graha Yudha).
    """
    
    def __init__(self):
        self.ep = EphemerisProvider()
        # Ensure we are checking absolute positions/separations
        
    def get_angular_separation(self, lon1, lon2):
        """Minimal separation on the circle (0-180)."""
        diff = abs(lon1 - lon2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def scan_yogas(self, planet_positions):
        """
        Input: dict of {PlanetName: Longitude}
        Output: List of Yoga objects/dicts
        """
        yogas = []
        
        # 1. Define Pairs of Interest for Financial/Mundane
        # (P1, P2, YogaName, Orb, Description)
        # Note: Orb for general conjunction is wide (e.g. same sign), 
        # but for intense effect we use effective orb (e.g. 5-8 deg).
        special_pairs = [
            ('Jupiter', 'True_Node', 'Guru-Chandal Yoga', 5.0, 'Market Corruption/Expansion Bubble'),
            ('Jupiter', 'Ketu', 'Ganesha Yoga', 5.0, 'Religious/Ethical Correction'), # Or Spritual
            ('Mars', 'True_Node', 'Angarak Yoga', 5.0, 'Violence/Explosive Volatility/Crashes'),
            ('Mars', 'Ketu', 'Pisacha Yoga', 5.0, 'Hidden Violence/Structural Breaks'),
            ('Saturn', 'Mars', 'Shani-Mangal Yoga', 5.0, 'Conflict/Recession/Hardship'),
            ('Saturn', 'True_Node', 'Shrapit Yoga', 5.0, 'Cursed/Destabilizing Force'),
            ('Sun', 'Saturn', 'Surya-Shani Yoga', 6.0, 'Government vs People/Authority Clashes'),
            ('Sun', 'True_Node', 'Grahan Yoga (Solar)', 8.0, 'Eclipsed Authority/Leadership Crisis'),
            ('Moon', 'True_Node', 'Grahan Yoga (Lunar)', 8.0, 'Public Panic/Sentiment Volatility')
        ]

        # Check Special Yogas
        for p1, p2, name, orb, desc in special_pairs:
            if p1 in planet_positions and p2 in planet_positions:
                sep = self.get_angular_separation(planet_positions[p1], planet_positions[p2])
                if sep <= orb:
                    # Intensity: closer = stronger
                    intensity = round((1 - (sep / orb)) * 100, 1)
                    yogas.append({
                        'Name': name,
                        'Type': 'Special Conjunction',
                        'Planets': [p1, p2],
                        'Separation': round(sep, 2),
                        'Intensity': intensity,
                        'Description': desc
                    })

        # 2. Planetary War (Graha Yudha)
        # Condition: Two *Non-Luminary* planets (Mars, Merc, Jup, Ven, Sat) within 1 degree.
        # Nodes and Sun/Moon are excluded from standard Yudha (though Sun causes combustion).
        combatants = ['Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        
        existing_pairs = list(itertools.combinations(combatants, 2))
        
        for p1, p2 in existing_pairs:
            if p1 in planet_positions and p2 in planet_positions:
                sep = self.get_angular_separation(planet_positions[p1], planet_positions[p2])
                if sep <= 1.0:
                    yogas.append({
                        'Name': f"Graha Yudha ({p1}-{p2})",
                        'Type': 'War',
                        'Planets': [p1, p2],
                        'Separation': round(sep, 3),
                        'Intensity': 100.0, # War is always intense
                        'Description': f"Planetary War between {p1} and {p2}. Conflict and instability."
                    })
                    
        return yogas

    def check_special_aspects(self, planet_positions):
        """
        Scans for Vedic Aspects (Drishti).
        Saturn: 3, 7, 10
        Mars: 4, 7, 8
        Jupiter: 5, 7, 9
        """
        aspects = []
        
        # Define Drishti Rules (Planet: [Aspects in Houses])
        # Converted to degrees (House * 30). Note: Vedic aspect is broadly by sign, 
        # but for high precision we check within an orb of the exact degree aspect.
        # e.g., Saturn aspects 3rd house -> +60 degrees.
        rules = {
            'Saturn': [60, 180, 270],
            'Mars': [90, 180, 210],
            'Jupiter': [120, 180, 240]
        }
        
        targets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'True_Node']
        
        for aspector, angles in rules.items():
            if aspector not in planet_positions: continue
            
            p1_lon = planet_positions[aspector]
            
            for angle in angles:
                # Calculate where the "Gaze" falls
                gaze_lon = (p1_lon + angle) % 360
                
                # Check if any target planet is near this gaze
                for target in targets:
                    if target == aspector: continue
                    if target not in planet_positions: continue
                    
                    p2_lon = planet_positions[target]
                    
                    # Distance between Gaze and Target
                    sep = self.get_angular_separation(gaze_lon, p2_lon)
                    
                    # Orb for Aspects: Tight (5 deg) for strong impact
                    if sep <= 5.0:
                        aspects.append({
                            'Name': f"{aspector} Aspects {target}",
                            'Type': 'Aspect',
                            'Planets': [aspector, target],
                            'Angle': angle,
                            'Separation': round(sep, 2),
                            'Description': f"{aspector} casts {angle}° glance on {target}"
                        })
                        
        return aspects
