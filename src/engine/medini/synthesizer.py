from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility
from src.engine.medini.yogas import YogaScanner
from src.engine.medini.temporal import TemporalScanner
from src.engine.medini.sector_mapper import SectorMapper
import swisseph as swe
import pandas as pd

class MediniSynthesizer:
    def __init__(self):
        self.ep = EphemerisProvider()
        self.ep.set_sidereal_mode(swe.SIDM_LAHIRI)
        
        self.yoga_scanner = YogaScanner()
        # YogaScanner inherits EP, we assume it picks up the set mode or we should enforce it 
        # Actually EphemerisProvider is a new instance inside them unless we pass it.
        # For simplicity in this architecture, they create their own.
        # We need to ensure they are all Sidereal.
        
        # Fixing architecture oversight: Set mode for all
        self.yoga_scanner.ep.set_sidereal_mode(swe.SIDM_LAHIRI)
        
        self.temporal_scanner = TemporalScanner()
        self.temporal_scanner.set_sidereal_mode(swe.SIDM_LAHIRI)
        
        self.mapper = SectorMapper()

    def generate_medini_report(self, date):
        """
        Generates a comprehensive report for the date.
        """
        # 1. Get Positions
        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'True_Node', 'Ketu']
        positions = {}
        full_info = {}
        
        for p in planets:
            lon, _, _, _ = self.ep.get_planet_data(date, p)
            if lon is not None:
                positions[p] = lon
                rasi, _, _ = ZodiacUtility.get_rasi(lon)
                full_info[p] = {'Lon': lon, 'Rasi': rasi}
                
        # 2. Scanning
        yogas = self.yoga_scanner.scan_yogas(positions)
        temporal_events = self.temporal_scanner.scan_temporal_events(date)
        
        # 3. Synthesis
        report = []
        
        # A. Yogas
        if yogas:
            report.append("### 🔥 ACTIVE YOGAS (Planetary Combinations)")
            for y in yogas:
                # Get sectors affected by involved planets
                impacts = []
                for p in y['Planets']:
                    impacts.append(SectorMapper.get_impact_description(p, y['Type']))
                
                impact_str = " | ".join(set(impacts))
                report.append(f"- **{y['Name']}** ({y['Description']})")
                report.append(f"  - *Sectors*: {impact_str}")
        
        # B. Temporal
        if temporal_events:
            report.append("### ⏳ TEMPORAL EVENTS")
            for t in temporal_events:
                report.append(f"- **{t['Type']}** (Axis: {t['Axis']})")
                
                # Eclipse Logic Synthesis
                if 'Eclipse' in t['Type']:
                    # Sun and Moon sectors hit
                    report.append(f"  - *Risk*: {SectorMapper.get_impact_description('Sun', 'Eclipse')}")
                    report.append(f"  - *Risk*: {SectorMapper.get_impact_description('Moon', 'Eclipse')}")
                    
        if not yogas and not temporal_events:
            report.append("### ✅ NO MAJOR DESTRUCTIVE PATTERNS DETECTED")
            
        return "\n".join(report)
