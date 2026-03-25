from src.engine.astro.core.ephemeris_provider import EphemerisProvider
import pandas as pd

class MundaneWeatherEngine:
    """
    Translates complex astronomical alignments into a single 
    'Sovereign Malefic Index' (SMI) for the Crash Predator.
    """
    def __init__(self):
        self.ep = EphemerisProvider()
        self.malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu']

    def calculate_smi(self, date, positions, dasha_md, dasha_ad):
        """
        Calculates the SMI (0 - 10.0 scale)
        """
        score = 0.0
        
        # 1. Planetary Wars (Graha Yuddha) - Mars and Saturn within 1 degree
        m_lon = positions.get('Mars')
        s_lon = positions.get('Saturn')
        if m_lon is not None and s_lon is not None:
            dist = self.ep.get_distance(m_lon, s_lon)
            if dist <= 1.0:
                score += 3.0 # High systemic danger
            elif dist <= 5.0:
                score += 1.0

        # 2. Malefic Dasha Logic (The Timing Layer)
        # S&P 500 / Nifty sensitivity to Saturn, Mars, Rahu, Ketu
        stress_lords = ['Saturn', 'Rahu', 'Ketu', 'Mars']
        
        from src.engine.medini.vedic_precision import VedicHighPrecisionEngine
        vpe = VedicHighPrecisionEngine()
        
        if dasha_md in stress_lords:
            # Apply Navamsha Debility & Sandhi multipliers
            m_lon = positions.get(dasha_md, 0)
            m_mult, b_strength = vpe.get_sign_multiplier(m_lon, market='INDIA')
            s_pulse = vpe.get_sandhi_pulse(m_lon)
            v_deb = vpe.get_varga_debility(m_lon)
            
            score += 2.0 * m_mult * s_pulse * v_deb
            
        if dasha_ad in stress_lords:
            a_lon = positions.get(dasha_ad, 0)
            a_mult, b_strength = vpe.get_sign_multiplier(a_lon, market='INDIA')
            score += 1.5 * a_mult

        # 3. Outer Planet Hard Aspects (Geocentric Sentiment)
        # Check Saturn-Neptune (Havoc Cycle)
        n_lon = positions.get('Neptune')
        if s_lon is not None and n_lon is not None:
            sn_dist = self.ep.get_distance(s_lon, n_lon)
            # Hard aspects: 0, 90, 180
            for aspect in [0, 90, 180]:
                if abs(sn_dist - aspect) <= 5.0:
                    score += 1.5
                    break

        # 4. Out of Bounds Intensity (OOB)
        # Handled in features.py, but we can add a basic check here for self-reliance
        # Logic: Malefics OOB = Chaos
        
        # Cap at 10.0
        return min(10.0, score)

    def get_weather_report(self, date, positions, dasha_md, dasha_ad):
        smi = self.calculate_smi(date, positions, dasha_md, dasha_ad)
        
        status = "CLEAR"
        if smi >= 8.0: status = "CRITICAL (STRUCTURAL FAILURE)"
        elif smi >= 6.0: status = "STORM (HIGH RISK)"
        elif smi >= 4.0: status = "OVERCAST (CAUTION)"
        
        return {
            'Sovereign_Malefic_Index': smi,
            'Astro_Weather_Status': status
        }
