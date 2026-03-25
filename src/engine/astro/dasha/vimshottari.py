from datetime import datetime, timedelta

class VimshottariDasha:
    """
    Vimshottari Dasha System (120 Years Cycle)
    Sequence: Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury
    """
    def __init__(self):
        self.dasha_years = {
            'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
            'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
        }
        self.sequence = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        # Nakshatra Lord Mapping (0=Ashwini -> Ketu)
        self.nak_lords = [
            'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
        ] * 3 
        
    def get_current_dasha(self, moon_lon, birth_date, target_date):
        """
        Calculate Mahadasha and Antardasha for a given date.
        moon_lon: Natal Moon Longitude (0-360)
        birth_date: datetime
        target_date: datetime
        """
        # 1. Calculate Nakshatra and Balance
        nak_idx = int(moon_lon / 13.333333)
        rem_deg = moon_lon % 13.333333
        percent_passed = rem_deg / 13.333333
        percent_remaining = 1.0 - percent_passed
        
        lord_idx = nak_idx % 9
        start_lord = self.nak_lords[nak_idx]
        
        balance_years = self.dasha_years[start_lord] * percent_remaining
        
        # 2. Iterate to Target Date
        curr_date = birth_date
        
        # First Dasha (Balance)
        curr_date += timedelta(days=balance_years * 365.25)
        if target_date < curr_date:
            return self._get_sub_periods(start_lord, birth_date, target_date, balance_years, is_balance=True)

        # Loop through sequence
        curr_lord_idx = (self.sequence.index(start_lord) + 1) % 9
        
        while True:
            lord = self.sequence[curr_lord_idx]
            duration = self.dasha_years[lord]
            end_date = curr_date + timedelta(days=duration * 365.25)
            
            if target_date <= end_date:
                # Found Mahadasha
                return self._get_sub_periods(lord, curr_date, target_date, duration)
                
            curr_date = end_date
            curr_lord_idx = (curr_lord_idx + 1) % 9
            
    def _get_sub_periods(self, md_lord, md_start_date, target_date, md_duration, is_balance=False):
        """
        Calculate Antardasha (Sub-Period)
        """
        # Antardasha Sequence starts from MD Lord
        start_idx = self.sequence.index(md_lord)
        
        curr_date = md_start_date
        
        # If it is a balance of dasha, the start date is birth date, but the "theoretical" start was earlier.
        # Use simple proportion for now. (Refining strictly for simplicity)
        
        # Standard Calculation
        for i in range(9):
            idx = (start_idx + i) % 9
            ad_lord = self.sequence[idx]
            
            # AD Years = (MD Years * AD Years) / 120
            ad_years = (self.dasha_years[md_lord] * self.dasha_years[ad_lord]) / 120.0
            
            end_date = curr_date + timedelta(days=ad_years * 365.25)
            
            if target_date <= end_date:
                return {
                    'Mahadasha': md_lord,
                    'Antardasha': ad_lord,
                    'MD_Start': md_start_date.strftime('%Y-%m-%d'),
                    'AD_End': end_date.strftime('%Y-%m-%d')
                }
            curr_date = end_date
            
        return {'Mahadasha': md_lord, 'Antardasha': 'Unknown'}

