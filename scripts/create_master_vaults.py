import yfinance as yf
import os
import pandas as pd

def create_master_vaults():
    root_dir = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5\data\raw"
    
    # 1. US MASTER
    us_master_dir = os.path.join(root_dir, "US", "MASTER")
    if not os.path.exists(us_master_dir): 
        os.makedirs(us_master_dir)
        print(f"Created US MASTER dir: {us_master_dir}")
    
    us_master_tickers = {
        "SP500_STANDARD": "^GSPC",
        "DOW_JONES_INDUSTRIAL": "^DJI",
        "NASDAQ_COMPOSITE": "^IXIC"
    }
    
    # 2. INDIA MASTER
    ind_master_dir = os.path.join(root_dir, "IND", "MASTER")
    if not os.path.exists(ind_master_dir): 
        os.makedirs(ind_master_dir)
        print(f"Created IND MASTER dir: {ind_master_dir}")
    
    ind_master_tickers = {
        "NIFTY_50_STANDARD": "^NSEI",
        "BSE_SENSEX_ESTABLISHMENT": "^BSESN",
        "NIFTY_500_BROAD": "NIFTY500.NS"
    }

    print("=== ACE: ESTABLISHING MASTER HISTORIC VAULTS (MAX-LIFE) ===")
    
    # Process US
    print("\n--- BUILDING US MASTER VAULT ---")
    for name, symbol in us_master_tickers.items():
        print(f"Acquiring {name} ({symbol})...")
        data = yf.download(symbol, period="max", interval="1d")
        if not data.empty:
            data.to_csv(os.path.join(us_master_dir, f"{name}.csv"))
            print(f"Locked Max Life: {len(data)} trading days.")

    # Process India
    print("\n--- BUILDING INDIA MASTER VAULT ---")
    for name, symbol in ind_master_tickers.items():
        print(f"Acquiring {name} ({symbol})...")
        p = "max" if symbol != "NIFTY500.NS" else "20y"
        data = yf.download(symbol, period=p, interval="1d")
        if not data.empty:
            data.to_csv(os.path.join(ind_master_dir, f"{name}.csv"))
            print(f"Locked Max Life: {len(data)} trading days.")

if __name__ == "__main__":
    create_master_vaults()
