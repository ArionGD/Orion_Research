"""
India Natal Chart Data - Independence Chart
This file contains the raw astrological data for India
"""
from datetime import datetime

# India Birth Data (Independence Chart)
INDIA_CHART = {
    'name': 'Republic of India',
    'chart_type': 'Independence Chart',
    'date': datetime(1947, 8, 15, 0, 0),  # August 15, 1947, 00:00 IST (Midnight)
    'location': {
        'city': 'New Delhi',
        'state': 'Delhi',
        'latitude': 28.6139,  # 28°37'N
        'longitude': 77.2090,  # 77°13'E
        'timezone': 'IST'  # Indian Standard Time (UTC+5:30)
    },
    'notes': 'India gained independence at midnight on August 15, 1947. Time: 00:00 IST = 18:30 UTC (Aug 14)'
}

# Pre-calculated Sidereal Lahiri positions (for reference/validation)
INDIA_INDEPENDENCE_POSITIONS = {
    'Ascendant': None,  # ~25° Taurus
    'MC': None,
    'Sun': None,  # Leo (Leadership)
    'Moon': None,  # Capricorn (Discipline/Structure)
    'Mercury': None,
    'Venus': None,  # Virgo
    'Mars': None,
    'Jupiter': None,  # Scorpio
    'Saturn': None,  # Cancer
    'Rahu': None,  # Taurus
    'Ketu': None
}

# Sensitive Points for India
INDIA_SENSITIVE_POINTS = {
    'Moon': 'Public sentiment, monsoon, agriculture',
    'Sun': 'Government, prime minister, national pride',
    'Saturn': 'Democracy, constitution, masses',
    'Jupiter': 'Economy, growth, education',
    'Mars': 'Military, borders, conflicts',
    'Ascendant': 'National identity, international image'
}
