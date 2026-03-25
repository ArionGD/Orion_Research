import numpy as np
import pandas as pd

class GannPriceTranslator:
    """
    Arion.ai: W.D. Gann 'Square of 9' Price-to-Longitude Translator
    ==============================================================
    Converts numerical price values into 360-degree circular coordinates.
    Logic: Based on the Gann Square Root Theory where:
    Angle = ((SQRT(Price) * 180) - 225) % 360
    
    This allows the engine to detect 'Collisions' between Price and Planet.
    """
    
    @staticmethod
    def calculate_price_longitude(price_series: pd.Series) -> pd.Series:
        """
        Vectorized conversion of a price series to zodiac degrees (0-360).
        Includes Scaled Wrapping for High-Magnitude indices (S&P 500/Nifty).
        """
        # Ensure price is positive and non-zero
        safe_price = np.where(price_series <= 0, 0.0001, price_series)
        
        # Determine the Scaling Factor (The 'Cycle of 9' levels)
        # Gann uses different 'scales' for different price ranges.
        # Level 1: Under 100
        # Level 10: Under 1000
        # Level 100: Under 10000 (e.g. S&P 500 at 5000)
        # We divide by magnitude factors to ensure the SQRT maps correctly.
        magnitude = 10 ** np.maximum(0, np.floor(np.log10(safe_price)) - 1)
        scaled_price = safe_price / magnitude
        
        # Gann Square Root Formula for Degrees:
        # √ScaledPrice * 180 converts the growth units to 360-degree rotation.
        # The -225 is the standard offset (Square Root of 2 is the first corner).
        degrees = (np.sqrt(scaled_price) * 180.0) - 225.0
        
        # Keep everything within the 0.0 to 359.99 range
        return degrees % 360.0

    @staticmethod
    def detect_price_time_collision(price_deg: float, planet_deg: float, tolerance: float = 1.0) -> bool:
        """
        Returns True if the Price Longitude matches a Planet Longitude within a tolerance.
        Checks for: Conjunction (0), Square (90), Opposition (180).
        """
        diff = abs(price_deg - planet_deg) % 360
        
        # Check standard hard aspects (Gann's 'Hard Angles')
        angles = [0, 90, 180, 270]
        for angle in angles:
            if abs(diff - angle) <= tolerance:
                return True
        return False

    def enrich_dataframe(self, df: pd.DataFrame, price_column: str = 'Close') -> pd.DataFrame:
        """
        Appends Gann Price-Degrees to the market dataframe.
        Optimized for massive Parquet files.
        """
        df_out = df.copy()
        df_out['Gann_Price_Deg'] = self.calculate_price_longitude(df_out[price_column])
        return df_out

# Implementation Example:
# translator = GannPriceTranslator()
# df = translator.enrich_dataframe(df)
# df['Price_Collision_Saturn'] = np.abs(df['Gann_Price_Deg'] - df['Saturn_Lon']) < 2.0
