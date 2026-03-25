import pandas as pd
import yfinance as yf
from tqdm import tqdm
import os

def build_data_forge():
    # 1. Universe Definition
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sp500 = sp500[['Symbol', 'GICS Sector']]
    
    sp400 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_400_companies')[0]
    if 'Ticker symbol' in sp400.columns:
        sp400.rename(columns={'Ticker symbol': 'Symbol'}, inplace=True)
    elif 'Ticker Symbol' in sp400.columns:
        sp400.rename(columns={'Ticker Symbol': 'Symbol'}, inplace=True)
    sp400 = sp400[['Symbol', 'GICS Sector']]
    
    universe = pd.concat([sp500, sp400]).drop_duplicates(subset=['Symbol'])
    universe['Symbol'] = universe['Symbol'].str.replace('.', '-', regex=False)
    
    # 2. $500M Valuation Filter
    surviving = []
    print("Filtering tickers by $500M Market Cap constraint...")
    for ticker, sector in tqdm(zip(universe['Symbol'], universe['GICS Sector']), total=len(universe)):
        try:
            info = yf.Ticker(ticker).info
            mcap = info.get('marketCap')
            if mcap and mcap >= 500_000_000:
                surviving.append({'Symbol': ticker, 'Sector': sector})
        except Exception:
            continue
    surviving_df = pd.DataFrame(surviving)
    
    # 3. Mass Ingestion
    tickers = surviving_df['Symbol'].tolist()
    sector_map = dict(zip(surviving_df['Symbol'], surviving_df['Sector']))
    
    print(f"Downloading historical data for {len(tickers)} surviving tickers...")
    raw_data = yf.download(tickers, period='max', threads=True)
    
    # 4. Data Cleaning & Formatting
    if isinstance(raw_data.columns, pd.MultiIndex):
        formatted_data = raw_data.stack(level=1, future_stack=True).reset_index()
        formatted_data.rename(columns={formatted_data.columns[1]: 'Ticker'}, inplace=True)
    else:
        formatted_data = raw_data.reset_index()
        formatted_data['Ticker'] = tickers[0]
        
    cols_to_keep = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']
    formatted_data = formatted_data[[c for c in cols_to_keep if c in formatted_data.columns]]
    
    formatted_data['Volume'] = formatted_data['Volume'].fillna(1).replace(0, 1)
    
    formatted_data['Sector'] = formatted_data['Ticker'].map(sector_map).fillna('Unknown')
    
    # 5. Sector-Specific Output
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'raw')
    os.makedirs(output_dir, exist_ok=True)
    
    sectors = formatted_data['Sector'].unique()
    print(f"Exporting to Parquet files in {os.path.abspath(output_dir)}...")
    for sector in sectors:
        safe_sector = str(sector).replace(' ', '_').replace('/', '_')
        sector_df = formatted_data[formatted_data['Sector'] == sector]
        
        output_path = os.path.join(output_dir, f"us_{safe_sector}_master.parquet")
        sector_df.to_parquet(output_path, engine='pyarrow', index=False)
        print(f"Saved: {output_path} ({len(sector_df)} records)")

if __name__ == "__main__":
    build_data_forge()
