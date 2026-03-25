class AshtakavargaCalculator:
    """
    Binna Ashtakavarga (BAV) Calculator
    Standard Parashara Rules for Points (Bindus)
    """
    def __init__(self):
        # Contribution Tables (Simplified for key planets)
        # 1 = Benefic Point given by Planet X to Sign Y (relative to itself)
        
        # Saturn's Contribution to itself and others
        self.saturn_points = {
            'Sun': [1, 2, 4, 7, 8, 10, 11],
            'Moon': [3, 6, 11],
            'Mars': [3, 5, 6, 10, 11, 12],
            'Mercury': [6, 8, 9, 10, 11, 12],
            'Jupiter': [5, 6, 11, 12],
            'Venus': [6, 11, 12],
            'Saturn': [3, 5, 6, 11],
            'Lagna': [1, 3, 4, 6, 10, 11]
        }
        
    def calculate_bav(self, planet, positions):
        """
        Calculate Points for a single planet (e.g., Saturn)
        in its current sign.
        """
        total_points = 0
        current_sign = int(positions[planet] / 30) + 1
        
        # Check contributions from all 7 planets + Lagna
        # For now, let's implement just Saturn's BAV as a proof of concept for "Crash Prediction"
        # Saturn weak (0-2 points) in transit sign = BAD.
        
        if planet == 'Saturn':
            contributors = self.saturn_points
            for donor, good_houses in contributors.items():
                if donor not in positions: continue
                
                donor_sign = int(positions[donor] / 30) + 1
                # Calculate which house Saturn is in relative to Donor
                # e.g. Saturn in Aries (1), Sun in Aries (1) -> 1st House.
                
                rel_house = (current_sign - donor_sign) + 1
                if rel_house <= 0: rel_house += 12
                
                if rel_house in good_houses:
                    total_points += 1
                    
        return total_points
