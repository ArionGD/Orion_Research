import pandas as pd
import numpy as np
from datetime import datetime, time

class GannWheelOf24:
    """
    Arion.ai Tier 2: INTRADAY TACTICAL ENGINE
    =========================================
    The 'Wheel of 24' completely divorces the Day-Trading logic from the 
    Macro 'Systemic Crash' (Medini) Engine.
    
    Logic: Gann discovered that 24 hours in a day maps identically to the 360° Zodiac.
    (360 / 24 = 15 degrees per hour).
    
    By mapping the exact minute of the day to a degree, we find where Intraday Price
    'Squares' the 'Time of Day', marking exact 5-min candle reversals.
    """
    
    def __init__(self, market_open_hour: int = 9, market_open_minute: int = 15):
        # Default aligned to NSE (Indian Markets) Open
        self.market_open = time(market_open_hour, market_open_minute)
        self.degrees_per_minute = 360.0 / (24 * 60) # 0.25 degrees per min
        
    def get_time_degree(self, current_time: datetime) -> float:
        """
        Converts the current time of day into a 360-degree circle coordinate.
        00:00 (Midnight) = 0°
        12:00 (Noon) = 180°
        """
        minutes_since_midnight = current_time.hour * 60 + current_time.minute
        time_degree = (minutes_since_midnight * self.degrees_per_minute) % 360.0
        return time_degree
        
    def calculate_intraday_pivots(self, opening_price: float) -> list:
        """
        Takes the Opening Price of the market and uses Gann's Square Root formula
        to find the 4 critical 'Intraday Vibration Nodes'.
        When the 'Time Degree' matches the 'Open Price Degree', a reversal happens.
        """
        # Convert Open Price to Gann Degrees
        safe_price = max(opening_price, 0.0001)
        price_deg = ((np.sqrt(safe_price) * 180.0) - 225.0) % 360.0
        
        # Calculate the 4 Hard Angles (Squaring) from the Open Price Deg
        pivot_degrees = [
            price_deg,                 # 0° (Conjunction: High Volatility Node)
            (price_deg + 90) % 360,    # 90° (Square: Support/Resistance Break)
            (price_deg + 180) % 360,   # 180° (Opposition: Mid-Day Trend Reversal)
            (price_deg + 270) % 360    # 270° (Square: Closing Trend Shift)
        ]
        
        return sorted(pivot_degrees)
        
    def convert_degree_to_time(self, degree: float) -> str:
        """
        Converts an intraday geometric Pivot Degree back into a wall-clock time 
        so the AI knows exactly which 5-minute candle to scan for a reversal.
        """
        total_minutes = int(degree / self.degrees_per_minute)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"
        
    def generate_daily_flight_plan(self, date: datetime, opening_price: float) -> dict:
        """
        Returns the exact Target Times (e.g. 10:35, 14:15) where the Wheel of 24
        predicts intra-day exhaustion tops and bottoms.
        """
        pivots = self.calculate_intraday_pivots(opening_price)
        reversal_times = [self.convert_degree_to_time(deg) for deg in pivots]
        
        return {
            "Date": date.strftime('%Y-%m-%d'),
            "Open_Price": opening_price,
            "Reversal_Candle_Times": reversal_times
        }

# Example Usage for Arion v4.8 Intraday Overlay
# wheel = GannWheelOf24()
# flight_plan = wheel.generate_daily_flight_plan(datetime.now(), 24500.0)
# print(flight_plan)
