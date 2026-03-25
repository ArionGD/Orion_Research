import pandas as pd
import numpy as np

class BradleySiderograph:
    """
    Arion.ai: Bradley Siderograph Accelerator
    =========================================
    The Bradley Siderograph is a mathematical model that assigns 
    numerical weights to planetary aspects to predict market energy.
    Positive (+): Trines (120), Sextiles (60)
    Negative (-): Squares (90), Oppositions (180)
    
    This replaces simple 'Sentiment' with 'Planetary Potential'.
    """
    
    # Standard Bradley Valencies (Simplified for Core Aspects)
    WEIGHTS = {
        'Conjunction': 0, # To be determined by planet pair
        'Sextile': 10,
        'Square': -15,
        'Trine': 15,
        'Opposition': -10
    }

    def __init__(self):
        # We target Outer Planet pairs (Jupiter, Saturn, Uranus, Neptune, Pluto)
        # for intermediate to long-term trend turning points.
        self.target_planets = ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']

    def calculate_pair_weight(self, p1_lon, p2_lon, p1_name, p2_name):
        """
        Calculates the Bradley valency for two planets based on their angular distance.
        """
        raw_diff = abs(p1_lon - p2_lon) % 360
        diff = min(raw_diff, 360 - raw_diff) # Circular distance
        
        # Check standard 5 aspects with an 8-degree orb
        orb = 8.0
        
        # Conjunction (0)
        if diff <= orb:
            # Bradley's specific rule: Conjunctions are pair-dependent
            # Jupiter/Uranus = Highly Bullish (+), Saturn/Pluto = Bearish (-)
            if p1_name == 'Jupiter' or p2_name == 'Jupiter': return 15
            if p1_name == 'Saturn' or p2_name == 'Saturn': return -15
            return 0
        
        if abs(diff - 60) <= orb: return self.WEIGHTS['Sextile']
        if abs(diff - 90) <= orb: return self.WEIGHTS['Square']
        if abs(diff - 120) <= orb: return self.WEIGHTS['Trine']
        if abs(diff - 180) <= orb: return self.WEIGHTS['Opposition']
        
        return 0

    def get_siderograph_score(self, planetary_positions: dict):
        """
        Aggregates sum for all unique pairs in target_planets.
        planetary_positions: { 'Jupiter': 120.5, 'Saturn': 90.1, ... }
        """
        score = 0
        from itertools import combinations
        
        pairs = list(combinations(self.target_planets, 2))
        for p1, p2 in pairs:
            if p1 in planetary_positions and p2 in planetary_positions:
                score += (self.calculate_pair_weight(
                         planetary_positions[p1], 
                         planetary_positions[p2], 
                         p1, p2))
                
        return score
