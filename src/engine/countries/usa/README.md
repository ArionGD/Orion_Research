# USA Country Module

This module provides country-specific astrological analysis for the United States.

## Structure

```
usa/
├── data.py          # Raw chart data and constants
├── profile.py       # Chart calculation engine
├── logic.py         # Transit-to-natal risk analysis
├── __init__.py      # Module exports
└── README.md        # This file
```

## Files

### data.py
**Purpose:** Store raw astrological data for USA  
**Contents:**
- `USA_CHART`: Birth data (Sibly Chart, July 4, 1776)
- `USA_SIBLY_POSITIONS`: Reference positions
- `USA_SENSITIVE_POINTS`: Key points for transit analysis

### profile.py
**Purpose:** Calculate natal positions from chart data  
**Key Class:** `USACountryProfile`  
**Methods:**
- `get_natal_positions()`: All planetary longitudes
- `get_sensitive_points()`: Key points (Moon, Sun, Saturn, etc.)
- `get_chart_info()`: Chart metadata

### logic.py
**Purpose:** Analyze transit-to-natal interactions  
**Key Class:** `USARiskEngine`  
**Methods:**
- `check_risk(transit_positions)`: Returns (score, signals)

**Checks:**
1. Sade Sati (Saturn on Moon)
2. Saturn on Sun (Authority Crisis)
3. Mars on Rahu (Violence/Panic)
4. Saturn Return (28-30 year cycle)

## Usage

```python
from src.engine.countries.usa import USARiskEngine

# Initialize
engine = USARiskEngine()

# Check risk for current transits
transit_positions = {'Saturn': 330.0, 'Mars': 45.0, ...}
score, signals = engine.check_risk(transit_positions)

print(f"USA Risk Score: {score}")
print(f"Signals: {signals}")
```

## Chart Information

**Chart:** Sibly Chart  
**Date:** July 4, 1776, 5:10 PM LMT  
**Location:** Philadelphia, PA (39.9526°N, 75.1652°W)  
**Ayanamsa:** Lahiri (Sidereal)

## Key Natal Points

- **Sun:** ~22° Gemini (Government/Authority)
- **Moon:** ~27° Aquarius (Public/Economy)
- **Ascendant:** ~8° Sagittarius (National Identity)
- **Saturn:** ~24° Virgo (Structure/Discipline)
- **Rahu:** ~18° Cancer (Obsession/Foreign Relations)

## Future Extensions

This architecture allows easy addition of:
- India module (`countries/india/`)
- China module (`countries/china/`)
- UK module (`countries/uk/`)

Each country module follows the same structure:
- `data.py`: Chart data
- `profile.py`: Calculation
- `logic.py`: Analysis
