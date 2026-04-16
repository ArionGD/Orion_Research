import yfinance as yf
import os
import pandas as pd

def populate_sovereign_vault():
    root_dir = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5\data\raw"
    
    # 1. USA TOP 7
    us_dir = os.path.join(root_dir, "US")
    if not os.path.exists(us_dir): os.makedirs(us_dir)
    
    us_tickers = {
        "TECH_QQQ": "QQQ",
        "BANKS_BKX": "^BKX",
        "SEMIS_SOX": "^SOX",
        "ENERGY_XLE": "XLE",
        "HEALTHCAR_XLV": "XLV",
        "CONSUMER_XLY": "XLY",
        "SMALLCAP_IWM": "IWM"
    }
    
    # 2. INDIA TOP 7
    ind_dir = os.path.join(root_dir, "IND")
    if not os.path.exists(ind_dir): os.makedirs(ind_dir)
    
    ind_tickers = {
        "BANKS_BANKNIFTY": "^NSEBANK",
        "IT_NIFTYIT": "^CNXIT",
        "METALS_NIFTYMETAL": "^CNXMETAL",
        "ENERGY_NIFTYENERGY": "^CNXENERGY",
        "PHARMA_NIFTYPHARMA": "^CNXPHARMA",
        "AUTO_NIFTYAUTO": "^CNXAUTO",
        "FMCG_NIFTYFMCG": "^CNXFMCG"
    }

    print("=== ACE: POPULATING MASTER SOVEREIGN VAULT (14 SECTORS) ===")
    
    # Process US
    print("\n--- SYNCING US VAULT ---")
    for name, symbol in us_tickers.items():
        print(f"Syncing {name}...")
        data = yf.download(symbol, period="max", interval="1d")
        if not data.empty:
            data.to_csv(os.path.join(us_dir, f"{name}.csv"))
            print(f"Done: {len(data)} trading days.")

    # Process India
    print("\n--- SYNCING INDIA VAULT ---")
    for name, symbol in ind_tickers.items():
        print(f"Syncing {name}...")
        data = yf.download(symbol, period="max", interval="1d")
        if not data.empty:
            data.to_csv(os.path.join(ind_dir, f"{name}.csv"))
            print(f"Done: {len(data)} trading days.")

    print("\n[COMPLETE] Master Sovereign Vault (Top 7 US + Top 7 India) is now locked.")

if __name__ == "__main__":
    populate_sovereign_vault()
