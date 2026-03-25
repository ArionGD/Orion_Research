class NeptuneLogic:
    """
    Neptune: The Dissolver. Representative of Confusion, Fraud, and Bubbles.
    In Financial Astrology: Inflation, Oil prices, Pharmaceutical scams, Market Delusions.
    """
    def check_bubble_risk(self, neptune_speed, aspects):
        """
        Neptune Stationary = Peak Confusion or Trend Reversal.
        """
        if neptune_speed is None: return 0, []
        score = 0
        signals = []
        if abs(neptune_speed) < 0.01:
            score += 10
            signals.append("Neptune Stationary (Trend Reversal/Illusion)")
            
        return score, signals
