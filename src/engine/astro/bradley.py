import numpy as np

class BradleyOscillator:
    """
    Arion.ai: Bradley Siderograph Master Oscillator (1948)
    =====================================================
    Weights the angular distance between planetary pairs to measure market 'Potential Energy'.
    Higher Value = Bullish Expansion Energy.
    Sharp Peaks/Troughs = Institutional Turning Points.
    """
    
    def __init__(self):
        # Bradley Weights for individual planets (Institutional standard)
        self.planet_weights = {
            'Venus': 4.0,
            'Mars': 3.0,
            'Jupiter': 5.0,
            'Saturn': -5.0, # Restriction
            'Uranus': -4.0, # Chaos
            'Neptune': -3.0 # Illusion/Panic
        }
        
    def calculate_bradley_score(self, planet_lons: dict) -> float:
        """
        Calculates the sum of weighted aspects between all specified planetary pairs.
        """
        planets = list(self.planet_weights.keys())
        total_score = 0.0
        
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                p1 = planets[i]
                p2 = planets[j]
                
                if p1 in planet_lons and p2 in planet_lons:
                    # Circular Distance
                    diff = abs(planet_lons[p1] - planet_lons[p2]) % 360
                    if diff > 180: diff = 360 - diff
                    
                    # Aspect Weights (Simplified Bradley logic)
                    aspect_power = 0
                    if diff < 10: aspect_power = 10 # Conjunction
                    elif abs(diff - 90) < 5: aspect_power = -5 # Square
                    elif abs(diff - 180) < 7: aspect_power = -8 # Opposition
                    elif abs(diff - 120) < 5: aspect_power = 8 # Trine
                    
                    # The Score is the product of the two planetary weights * aspect
                    pair_weight = self.planet_weights[p1] * self.planet_weights[p2]
                    total_score += pair_weight * aspect_power
                    
        return total_score

# translator = BradleyOscillator()
