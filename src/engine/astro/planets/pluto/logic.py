class PlutoLogic:
    """
    Pluto: The Destroyer. Representative of Debt, Power, and Transformation.
    In Financial Astrology: Banking Crises, Systemic Failure, Debt Implosions.
    """
    def check_systemic_risk(self, pluto_speed):
        """
        Pluto Stationary = Intense pressure on Grid/Banking.
        """
        if pluto_speed is None: return 0, []
        score = 0
        signals = []
        # Sensitivity Tuned for Daily Precision (v3.1)
        # Previous (0.005) was too strict for daily triggers. 
        # Widened to 0.008 to catch the 'slow down' phase before the crash.
        if abs(pluto_speed) < 0.007: 
            score += 20
            signals.append("Pluto Stationary (Systemic Threat)")
            
        return score, signals
