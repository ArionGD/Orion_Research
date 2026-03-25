import yfinance as yf
import pandas as pd
import os

def fetch_sp500():
    print("Fetching S&P 500 (^GSPC) data from Yahoo Finance...")
    
    # Check if we can fetch max history
    ticker = yf.Ticker("^GSPC")
    df = ticker.history(period="max")
    
    if df.empty:
        print("Error: No data fetched. Check network connection.")
        return
    
    # Save raw
    output_path = "data/raw/sp500_daily_full.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    print(f"Saved {len(df)} rows to {output_path}")
    print(f"Range: {df.index.min()} to {df.index.max()}")
    
    # Create Weekly Resampled Version (Friday Close)
    # Resample to Weekly 'W-FRI'
    weekly_df = df.resample('W-FRI').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    weekly_df.dropna(inplace=True)
    
    weekly_output = "data/raw/sp500_weekly_full.csv"
    weekly_df.to_csv(weekly_output)
    print(f"Saved {len(weekly_df)} weekly rows to {weekly_output}")

if __name__ == "__main__":
    fetch_sp500()
