"""
Country Manager - Multi-Country Orchestration
Provides unified interface for working with multiple country modules
"""

class CountryManager:
    """
    Manages multiple country modules and provides unified interface
    """
    def __init__(self):
        self.available_countries = {}
        self._load_countries()
        
    def _load_countries(self):
        """Load all available country modules"""
        try:
            from .usa import USARiskEngine
            self.available_countries['USA'] = USARiskEngine()
        except ImportError:
            pass
            
        try:
            from .india import IndiaRiskEngine
            self.available_countries['India'] = IndiaRiskEngine()
        except ImportError:
            pass
    
    def get_available_countries(self):
        """Returns list of available country names"""
        return list(self.available_countries.keys())
    
    def get_country_engine(self, country_name):
        """
        Returns the risk engine for a specific country
        Args:
            country_name: 'USA', 'India', etc.
        Returns:
            Risk engine instance or None
        """
        return self.available_countries.get(country_name)
    
    def check_risk(self, country_name, transit_positions):
        """
        Check risk for a specific country
        Args:
            country_name: 'USA', 'India', or None for global
            transit_positions: dict of current planetary positions
        Returns:
            (score, signals) tuple
        """
        if country_name is None or country_name == 'Global':
            return 0, []  # No country-specific risk for global
            
        engine = self.get_country_engine(country_name)
        if engine is None:
            return 0, []
            
        return engine.check_risk(transit_positions)
