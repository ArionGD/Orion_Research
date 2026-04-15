from src.engine.astro.eclipses.solar_eclipse.logic import SolarEclipseLogic
from src.engine.astro.eclipses.lunar_eclipse.logic import LunarEclipseLogic

class EclipseManager:
    def __init__(self):
        self.solar = SolarEclipseLogic()
        self.lunar = LunarEclipseLogic()
        
    def check_eclipses(self, date):
        """
        Returns total eclipse score and signals.
        """
        score = 0
        signals = []
        
        # Check Solar
        s_res = self.solar.check_eclipse(date)
        if s_res['Is_Eclipse']:
            score += s_res['Score']
            signals.append(s_res['Type'])
            
        # Check Lunar
        l_res = self.lunar.check_eclipse(date)
        if l_res['Is_Eclipse']:
            score += l_res['Score']
            signals.append(l_res['Type'])
            
        return score, signals
