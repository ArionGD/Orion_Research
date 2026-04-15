from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.yogas import YogaScanner
from src.engine.astro.eclipses.manager import EclipseManager
from src.engine.astro.chakra.sbc import SarvatobhadraChakra
from src.engine.medini.vedic_precision import VedicHighPrecisionEngine
from src.engine.medini.conflict_modifier import ConflictModifier
from src.engine.world.havoc_logic import GlobalHavocLogic
from datetime import timedelta
import pandas as pd

class MundaneWeatherEngine:
    """
    ULTRA PREDATOR v4.4 (Synthesis Level)
    Integrates: Yogas, SBC, Eclipses, Universal Havoc, and Conflict Modifiers.
    """
    def __init__(self):
        self.ep = EphemerisProvider()
        self.yoga_scanner = YogaScanner()
        self.eclipse_manager = EclipseManager()
        self.sbc_engine = SarvatobhadraChakra()
        self.vpe = VedicHighPrecisionEngine()
        self.conflict_mod = ConflictModifier()
        self.havoc_logic = GlobalHavocLogic()

    def calculate_smi(self, date, positions, dasha_md, dasha_ad, market='INDIA'):
        """
        Calculates the SMI (0 - 10.0 scale) via v4.4 Synthesis Logic.
        """
        score = 0.0
        
        # 1. Havoc (Layer 4)
        prev_date = date - timedelta(days=1)
        havoc_data = self.havoc_logic.calculate_havoc_features(date, prev_date)
        if havoc_data:
            gsi = havoc_data.get('Global_Stability_Index', 900)
            if gsi < 780: score += 1.5
            if abs(havoc_data.get('Havoc_Velocity', 0)) > 20: score += 1.0

        # 2. Conflict (Layer 3)
        conflict_analysis = self.conflict_mod.analyze_conflict(positions, date)
        if conflict_analysis['conflict_active']:
            score += 2.0 if conflict_analysis['conflict_type'] == 'hot_war' else 1.0

        # 3. Yogas (Layer 1)
        yogas = self.yoga_scanner.scan_yogas(positions)
        for y in yogas:
            if y['Type'] == 'War': score += 3.5
            elif y['Intensity'] > 80: score += 1.5

        # 4. SBC (Layer 2)
        sbc_score, _ = self.sbc_engine.check_crash_vedha(positions)
        score += min(2.5, sbc_score / 6.0)

        # 5. Dasha & Multiplier
        m_lon = positions.get(dasha_md, 0)
        m_mult, strength = self.vpe.get_sign_multiplier(m_lon, market=market)
        
        # Base multiplier for Rahu/Saturn dashas
        malefics = ['Saturn', 'Rahu', 'Ketu', 'Mars']
        base_d = 1.5 if dasha_md in malefics else 0.5
        score += base_d * m_mult

        # Cap
        return round(min(10.0, score), 2)

    def get_weather_report(self, date, positions, dasha_md, dasha_ad, market='INDIA'):
        smi = self.calculate_smi(date, positions, dasha_md, dasha_ad, market=market)
        
        status = "CLEAR"
        target = "LONG EQUITY"
        recommendation = "ACCUMULATE DCA"
        
        if smi >= 8.5:
            status = "CRITICAL (STRUCTURAL RESET)"
            target = "NASDAQ 100 (QQQ) PUTS" if market == 'US' else "BANK NIFTY (MCL) PUTS"
            recommendation = f"THE BIG SHORT: 15X ALPHA STRIKE ON {target}."
        elif smi >= 6.5:
            status = "STORM (HIGH VOLATILITY)"
            target = "GOLD / DEFENCE"
            recommendation = "HEDGE PORTFOLIO. MOVE TO CASH."
            
        return {
            'Sovereign_Malefic_Index': smi,
            'Astro_Weather_Status': status,
            'Target_Index': target,
            'Recommendation': recommendation
        }
