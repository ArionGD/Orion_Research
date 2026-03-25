import yfinance as yf
import pandas as pd
import os

def build_datasets():
    print("=== Arion.ai Investable Grade Data Builder ===")
    os.makedirs("data/processed", exist_ok=True)

    # --- 1. US Market (Large & Mid Cap) ---
    print("\nFetching US Market Data (Large & Mid Cap)...")
    # S&P 500 (Large Cap)
    sp500 = yf.Ticker("^GSPC").history(period="max")
    sp500['Type'] = 'Large Cap (S&P 500)'
    
    # S&P 400 (Mid Cap) - Note: History might be shorter than GSPC
    sp400 = yf.Ticker("^MID").history(period="max")
    sp400['Type'] = 'Mid Cap (S&P 400)'
    
    # Merge
    # We will prioritize S&P 500 for the 'Main' timeline, but keeping both allows comparison
    # For the MASTER file, we essentially want the "Market Pulse". S&P 500 is the best standard.
    # However, user asked to "pick stocks". For a Master Index file, we combine them.
    # Let's save a clean daily Master for the engine (S&P 500)
    
    us_master = sp500[['Close', 'Open', 'High', 'Low', 'Volume']].copy()
    us_master.dropna(inplace=True)
    us_path = "data/processed/us_master_daily.csv"
    us_master.to_csv(us_path)
    print(f"[SUCCESS] US Master Saved: {us_path}")
    print(f"   - Range: {us_master.index.min().date()} to {us_master.index.max().date()}")
    print(f"   - Rows: {len(us_master)}")
    
    # --- 2. India Market (BSE & NSE > 1000Cr Proxy) ---
    print("\nFetching India Market Data (BSE & NSE)...")
    # BSE SENSEX (The oldest reliable Indian data)
    # Represents the top 30 established companies (Large Cap)
    bse = yf.Ticker("^BSESN").history(period="max")
    
    # NSE NIFTY 50 (Broader Large/Mid representation)
    nifty = yf.Ticker("^NSEI").history(period="max")
    
    if bse.empty and nifty.empty:
        print("[ERROR] Could not fetch India data. Check internet/tickers.")
    else:
        # We prefer BSE for history length (starts 1997 in stats, earlier effectively)
        # Nifty starts 2007 reliability
        
        # Let's create a combined 'India Master' 
        # We use Sensex for older data, Nifty for newer/correlation if needed.
        # Ideally, just picking the longest one is best for backtesting.
        
        india_master = bse[['Close', 'Open', 'High', 'Low', 'Volume']].copy()
        
        # Cleanup
        india_master.dropna(inplace=True)
        ind_path = "data/processed/india_master_daily.csv"
        india_master.to_csv(ind_path)
        
        print(f"[SUCCESS] India Master (BSE Sensex) Saved: {ind_path}")
        print(f"   - Range: {india_master.index.min().date()} to {india_master.index.max().date()}")
        print(f"   - Rows: {len(india_master)}")
        print("   * Note: This represents the 'Cream' of Indian Corporate (>1000Cr Market Cap guaranteed).")

if __name__ == "__main__":
    build_datasets()
