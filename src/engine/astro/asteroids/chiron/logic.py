class ChironLogic:
    """
    Chiron: The Maverick / Wounded Healer.
    In Financial Astrology: Key indicator of 'Turnarounds', bottoms, or specific sector healing.
    """
    def check_turnaround(self, speed):
        if speed is None: return 0, []
        score = 0
        signals = []
        if abs(speed) < 0.005:
            score += 5
            signals.append("Chiron Stationary (Turnaround Zone)")
        return score, signals
