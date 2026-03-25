"""
USA Natal Chart Profile - Calculation Engine
This module handles the calculation of USA natal positions from the raw chart data
"""
import swisseph as swe
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from .data import USA_CHART

class USACountryProfile:
    """
    Calculates and provides USA Natal Chart positions.
    Uses the Sibly Chart data from data.py
    """
    def __init__(self):
        self.ep = EphemerisProvider()
        self.ep.set_sidereal_mode()  # Ensure Sidereal Lahiri
        
        # Load USA chart data
        self.chart_data = USA_CHART
        self.date = self.chart_data['date']
        self.lat = self.chart_data['location']['latitude']
        self.lon = self.chart_data['location']['longitude']
        
        # Calculate natal positions on initialization
        self.natal_positions = self._calculate_natal()
        
    def _calculate_natal(self):
        """
        Calculate all planetary positions for USA birth chart
        LMT = Local Mean Time conversion:
        Philadelphia: 75.1652°W / 15 = 5.011 hours (5h 0m 40s west)
        17:10 LMT = 22:10:40 UTC
        """
        # Convert LMT to UTC
        jd = swe.julday(1776, 7, 4, 22.177)  # 22h + 10.6min/60
        
        positions = {}
        for p_name, pid in self.ep.planet_ids.items():
            # Skip Chiron for 1776 (limited precision/relevance)
            if p_name == 'Chiron':
                continue
                
            try:
                res, _ = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_SPEED)
                positions[p_name] = res[0]
            except:
                positions[p_name] = None
                
        return positions
        
    def get_natal_positions(self):
        """Returns all calculated natal positions"""
        return self.natal_positions
        
    def get_sensitive_points(self):
        """
        Returns the most sensitive points in USA chart for transit analysis
        These are the key positions that transits interact with
        """
        return {
            'Ascendant': 248.0,  # ~8° Sagittarius (Sibly)
            'Moon': self.natal_positions.get('Moon'),      # Public/Economy
            'Sun': self.natal_positions.get('Sun'),        # Government/Authority
            'Saturn': self.natal_positions.get('Saturn'),  # Structure/Karma
            'Rahu': self.natal_positions.get('True_Node')  # Obsession/Foreign
        }
    
    def get_chart_info(self):
        """Returns reference information about the chart"""
        return {
            'name': self.chart_data['name'],
            'type': self.chart_data['chart_type'],
            'date': self.chart_data['date'].strftime('%B %d, %Y %H:%M %Z'),
            'location': f"{self.chart_data['location']['city']}, {self.chart_data['location']['state']}",
            'coordinates': f"{self.lat}°N, {abs(self.lon)}°W"
        }
