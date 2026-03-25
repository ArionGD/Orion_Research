"""
Conflict Modifier for Medini Engine v4.4
=========================================
Detects War/Conflict signatures from planetary data and determines
whether the scenario is a SUPPLY SHOCK (hot war) or DEMAND DESTRUCTION (cold siege).

This directly addresses the March 2026 failure where:
- The engine predicted Energy would HOLD/fall (demand destruction thesis)
- Reality: A hot war (US-Israel-Iran) caused a SUPPLY SHOCK, spiking oil +46%

Root Logic:
- Mars dominant over Saturn → HOT WAR → Supply Shock → Energy SPIKES
- Saturn dominant over Mars → COLD SIEGE → Demand Destruction → Energy CRASHES
- Both scenarios → Risk-Off for Tech, Auto, Banking, Real Estate
"""

from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.yogas import YogaScanner
import swisseph as swe


class ConflictModifier:
    """
    Analyzes Mars-Saturn dynamics to determine war type and adjust sector scores.
    """

    # Sign dignities for Mars and Saturn (sidereal longitudes)
    MARS_DIGNITY = {
        'exalted': (270, 300),      # Capricorn
        'own_aries': (0, 30),       # Aries
        'own_scorpio': (210, 240),  # Scorpio
        'debilitated': (90, 120),   # Cancer
    }

    SATURN_DIGNITY = {
        'exalted': (180, 210),      # Libra
        'own_aquarius': (300, 330),  # Aquarius
        'own_capricorn': (270, 300), # Capricorn
        'debilitated': (0, 30),     # Aries
    }

    # Hard aspect angles and their orbs
    HARD_ASPECTS = {
        'conjunction': {'angle': 0, 'orb': 10},
        'opposition': {'angle': 180, 'orb': 10},
        'square': {'angle': 90, 'orb': 8},
    }

    def __init__(self):
        self.ep = EphemerisProvider()
        self.ep.set_sidereal_mode(swe.SIDM_LAHIRI)
        self.yoga_scanner = YogaScanner()

    def _get_angular_separation(self, lon1, lon2):
        """Minimal separation on the circle (0-180)."""
        diff = abs(lon1 - lon2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def _check_dignity(self, planet, lon, dignity_map):
        """
        Returns a dignity score for a planet:
        +2 = Exalted, +1 = Own Sign, 0 = Neutral, -1 = Debilitated
        """
        for dignity, (start, end) in dignity_map.items():
            if start <= lon < end:
                if 'exalted' in dignity:
                    return 2
                elif 'own' in dignity:
                    return 1
                elif 'debilitated' in dignity:
                    return -1
        return 0

    def _check_hard_aspect(self, mars_lon, saturn_lon):
        """
        Checks if Mars and Saturn are in a hard aspect.
        Returns: (aspect_name, separation, intensity) or None
        """
        sep = self._get_angular_separation(mars_lon, saturn_lon)

        for aspect_name, config in self.HARD_ASPECTS.items():
            target_angle = config['angle']
            orb = config['orb']

            # For conjunction, check distance from 0
            if target_angle == 0:
                if sep <= orb:
                    intensity = round((1 - (sep / orb)) * 100, 1)
                    return (aspect_name, sep, intensity)
            else:
                # For opposition/square, check distance from target angle
                if abs(sep - target_angle) <= orb:
                    intensity = round((1 - (abs(sep - target_angle) / orb)) * 100, 1)
                    return (aspect_name, sep, intensity)

        return None

    def analyze_conflict(self, planet_positions, date=None):
        """
        Main analysis function.

        Returns a dict with:
        - conflict_active: bool
        - conflict_type: 'hot_war' | 'cold_siege' | None
        - mars_strength: int (dignity score)
        - saturn_strength: int (dignity score)
        - aspect: str (conjunction/opposition/square)
        - intensity: float (0-100)
        - sector_modifiers: dict of {sector: score_adjustment}
        - signals: list of human-readable signal strings
        """
        result = {
            'conflict_active': False,
            'conflict_type': None,
            'mars_strength': 0,
            'saturn_strength': 0,
            'aspect': None,
            'intensity': 0,
            'sector_modifiers': {},
            'signals': []
        }

        mars_lon = planet_positions.get('Mars')
        saturn_lon = planet_positions.get('Saturn')

        if mars_lon is None or saturn_lon is None:
            return result

        # 1. Check if Mars-Saturn are in a hard aspect
        aspect_result = self._check_hard_aspect(mars_lon, saturn_lon)

        if aspect_result is None:
            # No hard aspect — check if they're approaching one (applying)
            # For now, no conflict detected without hard aspect
            return result

        aspect_name, separation, intensity = aspect_result
        result['conflict_active'] = True
        result['aspect'] = aspect_name
        result['intensity'] = intensity

        # 2. Determine Mars vs Saturn strength
        mars_dignity = self._check_dignity('Mars', mars_lon, self.MARS_DIGNITY)
        saturn_dignity = self._check_dignity('Saturn', saturn_lon, self.SATURN_DIGNITY)

        # Also check speed — faster planet is more "active"
        mars_speed = None
        saturn_speed = None
        if date is not None:
            _, mars_speed, _, _ = self.ep.get_planet_data(date, 'Mars')
            _, saturn_speed, _, _ = self.ep.get_planet_data(date, 'Saturn')

        # Composite strength score
        mars_score = mars_dignity * 2
        saturn_score = saturn_dignity * 2

        if mars_speed is not None and saturn_speed is not None:
            # Faster planet gets a bonus (Mars is typically ~0.5 deg/day, Saturn ~0.03)
            if abs(mars_speed) > 0.4:
                mars_score += 1  # Mars is at normal speed (active)
            if mars_speed < 0:
                mars_score -= 1  # Retrograde Mars = weakened aggression

            if saturn_speed < 0:
                saturn_score += 1  # Retrograde Saturn = intensified restriction

        # Check Rahu involvement (amplifies chaos)
        rahu_lon = planet_positions.get('True_Node')
        rahu_boost = 0
        if rahu_lon is not None:
            rahu_mars_sep = self._get_angular_separation(mars_lon, rahu_lon)
            if rahu_mars_sep < 15:
                rahu_boost = 2  # Angarak Yoga — amplifies Mars violence
                mars_score += rahu_boost
                result['signals'].append("Rahu-Mars proximity (Angarak) — amplified conflict intensity")

        result['mars_strength'] = mars_score
        result['saturn_strength'] = saturn_score

        # 3. Determine conflict type
        if mars_score > saturn_score:
            result['conflict_type'] = 'hot_war'
            result['signals'].append(
                f"Mars dominant ({mars_score} vs Saturn {saturn_score}) → HOT WAR scenario"
            )
        elif saturn_score > mars_score:
            result['conflict_type'] = 'cold_siege'
            result['signals'].append(
                f"Saturn dominant ({saturn_score} vs Mars {mars_score}) → COLD SIEGE scenario"
            )
        else:
            # Equal — defaults to cold_siege (Saturn is the natural malefic restrictor)
            result['conflict_type'] = 'cold_siege'
            result['signals'].append(
                "Mars-Saturn equal strength → defaulting to COLD SIEGE (Saturn restricts)"
            )

        # 4. Calculate sector modifiers based on conflict type
        scale = intensity / 100.0  # 0.0 to 1.0 based on aspect tightness

        if result['conflict_type'] == 'hot_war':
            # HOT WAR: Supply shock, military spending, commodity spike
            result['sector_modifiers'] = {
                'Energy & Metals': round(8 * scale),      # OIL SPIKES (supply shock)
                'Tech & AI': round(-6 * scale),            # Risk-off selloff
                'Auto & Transport': round(-7 * scale),     # Rising fuel costs crush margins
                'Banking & Finance': round(-5 * scale),    # Credit risk, FII outflows
                'Real Estate': round(-6 * scale),          # Rate hike fears, risk-off
                'Pharma & Health': round(3 * scale),       # Defensive play
            }
            result['signals'].extend([
                "Energy: SUPPLY SHOCK — oil prices spike due to war disruption",
                "Tech/Auto/Banks: RISK-OFF — global capital flees to safety",
                "Pharma: Defensive rotation inflows"
            ])

        elif result['conflict_type'] == 'cold_siege':
            # COLD SIEGE: Demand destruction, economic freeze
            result['sector_modifiers'] = {
                'Energy & Metals': round(-7 * scale),      # Demand destruction
                'Tech & AI': round(-4 * scale),            # Recession fear
                'Auto & Transport': round(-4 * scale),     # Demand slowdown
                'Banking & Finance': round(-3 * scale),    # Credit contraction
                'Real Estate': round(-5 * scale),          # Stagnation
                'Pharma & Health': round(2 * scale),       # Defensive
            }
            result['signals'].extend([
                "Energy: DEMAND DESTRUCTION — factories stop, oil demand collapses",
                "All cyclicals: Recession fear driven selloff",
            ])

        return result

    def get_summary(self, analysis):
        """Returns a human-readable summary of the conflict analysis."""
        if not analysis['conflict_active']:
            return "No active Mars-Saturn conflict detected."

        lines = []
        lines.append(f"⚔️ CONFLICT ACTIVE: {analysis['conflict_type'].upper().replace('_', ' ')}")
        lines.append(f"   Aspect: Mars-Saturn {analysis['aspect']} (Intensity: {analysis['intensity']}%)")
        lines.append(f"   Mars Strength: {analysis['mars_strength']}, Saturn Strength: {analysis['saturn_strength']}")
        lines.append("")
        lines.append("   Sector Adjustments:")
        for sector, modifier in analysis['sector_modifiers'].items():
            direction = "↑" if modifier > 0 else "↓"
            lines.append(f"   {direction} {sector}: {modifier:+d}")
        lines.append("")
        lines.append("   Signals:")
        for sig in analysis['signals']:
            lines.append(f"   • {sig}")

        return "\n".join(lines)
