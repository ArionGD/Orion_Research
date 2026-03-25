class SectorMapper:
    """
    Maps Planets to Financial Sectors according to Medini Jyotish.
    """
    
    SECTOR_MAP = {
        'Sun': ['Government Bonds', 'Public Sector Units (PSU)', 'Gold', 'Wheat', 'Pharma (Generics)'],
        'Moon': ['FMCG', 'Hospitality', 'Shipping', 'Dairy/Liquids', 'Silver'],
        'Mars': ['Defense/Aerospace', 'Real Estate', 'Crypto/Blockchain', 'Metals (Copper/Steel)', 'Energy (Oil)', 'Sports'],
        'Mercury': ['IT/Software', 'Telecom', 'Media/Publishing', 'Logistics', 'Textiles', 'EdTech'],
        'Jupiter': ['Banking/Finance', 'Law/Legal', 'Education', 'Sugar/Food', 'Treasury'],
        'Venus': ['Luxury Goods', 'Automobiles', 'Entertainment', 'Fashion', 'Aviation', 'Forex'],
        'Saturn': ['Mining/Minerals', 'Infrastructure', 'Cement', 'Coal/Oil', 'Labor-Intensive', 'Waste Mgmt'],
        'Rahu': ['AI/Tech', 'Pharma (R&D)', 'Space Tech', 'Speculative', 'Electronics', 'Chemicals'],
        'Ketu': ['Medical Devices', 'Spiritual/Wellness', 'Micro-biology', 'Encryption', 'Bankruptcy Services']
    }
    
    @staticmethod
    def get_sectors_for_planet(planet_name):
        return SectorMapper.SECTOR_MAP.get(planet_name, [])
        
    @staticmethod
    def get_impact_description(planet, yoga_type):
        """
        Returns a financial impact string based on the planet and effect type.
        """
        base_sectors = ", ".join(SectorMapper.SECTOR_MAP.get(planet, [])[:3])
        
        if 'Conjunction' in yoga_type or 'War' in yoga_type:
            return f"⚠️ VOLATILITY ALERT: {base_sectors}"
        if 'Eclipse' in yoga_type:
             return f"🔻 SUDDEN DIP RISK: {base_sectors}"
        return f"Influence on {base_sectors}"
