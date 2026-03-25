import pandas as pd
import numpy as np

class ArionVirtualBroker:
    def __init__(self, c=0.1, taxes=0.0011, base_slippage=0.0005):
        self.c = c
        self.taxes = taxes
        self.base_slippage = base_slippage

    def apply_friction(self, df: pd.DataFrame, order_qty: int) -> pd.DataFrame:
        safe_adv = np.where(df['Volume'] == 0, 1, df['Volume'])
        sigma = (df['High'] - df['Low']) / df['Close']
        market_impact = self.c * sigma * np.sqrt(order_qty / safe_adv)
        
        total_friction = self.base_slippage + market_impact + self.taxes
        
        df_out = df.copy()
        df_out['Market_Impact'] = market_impact
        df_out['Arion_Buy_Price'] = df_out['Close'] * (1 + total_friction)
        df_out['Arion_Sell_Price'] = df_out['Close'] * (1 - total_friction)
        
        return df_out

# Example Usage:
# broker = ArionVirtualBroker()
# df = broker.apply_friction(df, order_qty=5000)
