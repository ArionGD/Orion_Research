class UranusLogic:
    """
    Uranus: The Awakener. Representative of Shock, Disruption, and Technology shocks.
    In Financial Astrology: Sudden Volatility, Flash Crashes, Breakouts.
    """
    def calculate_risk(self, position_data):
        """
        Input: { 'Uranus': deg, 'Aspects': ... } provided by caller or fetched internally if needed.
        But for consistency with v2 architecture, we might process raw position/aspects here
        or just return a base score based on Sign/Nakshatra.
        
        For now, let's keep it simple: Volatility Score based on aspects.
        """
        # Placeholder for sophisticated logic
        # In a real engine, we'd check:
        # 1. Is Uranus Stationary? (Flash Crash Signal)
        # 2. Is Uranus aspecting Mars?
        return {
            'Uranus_Score': 0, # To be populated by Aspect Scanner mainly
            'Signals': []
        }
        
    def check_volatility(self, uranus_speed):
        """
        High Risk if Uranus slows down (Stationary).
        """
        if uranus_speed is None: return 0, []
        score = 0
        signals = []
        # Sensitivity Tuned for Daily Precision (v3.1)
        # Previous (0.01) missed 1987 speed deceleration.
        # Widened to 0.04 to capture the 'Flash Crash' window.
        if abs(uranus_speed) < 0.04:
            score += 15
            signals.append("Uranus Stationary (High Volatility)")
        return score, signals
