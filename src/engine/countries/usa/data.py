"""
USA Natal Chart Data - Sibly Chart
This file contains the raw astrological data for the United States
"""
from datetime import datetime

# USA Birth Data (Sibly Chart)
USA_CHART = {
    'name': 'United States of America',
    'chart_type': 'Sibly Chart',
    'date': datetime(1776, 7, 4, 17, 10),  # July 4, 1776, 5:10 PM LMT
    'location': {
        'city': 'Philadelphia',
        'state': 'Pennsylvania',
        'latitude': 39.9526,  # 39°52'N
        'longitude': -75.1652,  # 75°10'W
        'timezone': 'LMT'  # Local Mean Time
    },
    'notes': 'Standard Sibly Chart for USA. Time converted to UTC: ~22:10:40'
}

# Pre-calculated Sidereal Lahiri positions (for reference/validation)
# These are approximate and should be verified by calculation
USA_SIBLY_POSITIONS = {
    'Ascendant': 248.0,  # ~8° Sagittarius
    'MC': None,  # To be calculated
    'Sun': None,  # ~22° Gemini (Sidereal Lahiri)
    'Moon': None,  # ~27° Aquarius
    'Mercury': None,
    'Venus': None,
    'Mars': None,  # ~0° Gemini
    'Jupiter': None,
    'Saturn': None,  # ~24° Virgo
    'Rahu': None,  # ~18° Cancer
    'Ketu': None
}

# Sensitive Points for USA
USA_SENSITIVE_POINTS = {
    'Moon': 'Public sentiment, economy',
    'Sun': 'Government, authority, leadership',
    'Saturn': '10th Lord - structure, karma',
    'Rahu': 'Obsession, technology, foreign affairs',
    'Ascendant': 'National identity'
}
