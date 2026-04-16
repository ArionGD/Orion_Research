import yfinance as yf
import os
import pandas as pd

def download_india_sectors():
    target_dir = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5\data\raw\IND"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created directory: {target_dir}")

    # Tickers: Bank Nifty, Nifty IT, Nifty Pharma, Energy, Auto, FMCG
    tickers = {
        "BANK_NIFTY": "^NSEBANK",
        "NIFTY_IT": "^CNXIT",
        "NIFTY_PHARMA": "^CNXPHARMA",
        "NIFTY_ENERGY": "^CNXENERGY",
        "NIFTY_AUTO": "^CNXAUTO",
        "NIFTY_FMCG": "^CNXFMCG",
        "NIFTY_50": "^NSEI" # Added for benchmark
    }

    print("=== ACE: INDIA SECTOR DATA ACQUISITION ===")
    
    for name, symbol in tickers.items():
        print(f"Downloading {name} ({symbol})...")
        try:
            data = yf.download(symbol, period="max", interval="1d")
            if data.empty:
                print(f"Warning: No data found for {symbol}")
                continue
                
            file_path = os.path.join(target_dir, f"{name}_daily.csv")
            data.to_csv(file_path)
            print(f"Successfully saved {name} to {file_path} ({len(data)} rows)")
        except Exception as e:
            print(f"Error downloading {symbol}: {e}")

    print("\n[COMPLETE] India Sovereign Sector Vault populated.")

if __name__ == "__main__":
    download_india_sectors()
