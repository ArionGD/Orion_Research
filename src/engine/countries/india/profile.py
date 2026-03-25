"""
India Natal Chart Profile - Calculation Engine
Calculates natal positions for India's Independence Chart
"""
import swisseph as swe
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from .data import INDIA_CHART

class IndiaCountryProfile:
    """
    Calculates and provides India Natal Chart positions.
    Uses the Independence Chart (August 15, 1947 midnight)
    """
    def __init__(self):
        self.ep = EphemerisProvider()
        self.ep.set_sidereal_mode()  # Sidereal Lahiri
        
        # Load India chart data
        self.chart_data = INDIA_CHART
        self.date = self.chart_data['date']
        self.lat = self.chart_data['location']['latitude']
        self.lon = self.chart_data['location']['longitude']
        
        # Calculate natal positions
        self.natal_positions = self._calculate_natal()
        
    def _calculate_natal(self):
        """
        Calculate all planetary positions for India Independence chart
        August 15, 1947, 00:00 IST (Midnight)
        IST = UTC+5:30, so 00:00 IST = August 14, 18:30 UTC
        """
        # Convert IST to UTC: 00:00 - 5:30 = 18:30 previous day
        jd = swe.julday(1947, 8, 14, 18.5)  # Aug 14, 18:30 UTC
        
        positions = {}
        for p_name, pid in self.ep.planet_ids.items():
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
        Returns the most sensitive points in India chart for transit analysis
        """
        return {
            'Ascendant': None,  # To be calculated from houses
            'Moon': self.natal_positions.get('Moon'),      # Public/Masses
            'Sun': self.natal_positions.get('Sun'),        # Government/PM
            'Mercury': self.natal_positions.get('Mercury'), # Trade/IT/Comms
            'Saturn': self.natal_positions.get('Saturn'),  # Democracy/Constitution
            'Jupiter': self.natal_positions.get('Jupiter'), # Economy/Growth
            'Mars': self.natal_positions.get('Mars'),      # Military/Borders
            'Rahu': self.natal_positions.get('True_Node')  # Foreign/Technology
        }
    
    def get_chart_info(self):
        """Returns reference information about the chart"""
        return {
            'name': self.chart_data['name'],
            'type': self.chart_data['chart_type'],
            'date': self.chart_data['date'].strftime('%B %d, %Y %H:%M %Z'),
            'location': f"{self.chart_data['location']['city']}, {self.chart_data['location']['state']}",
            'coordinates': f"{self.lat}°N, {self.lon}°E"
        }
