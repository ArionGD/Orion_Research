import yfinance as yf
import pandas as pd
import numpy as np
import swisseph as swe
import os
from datetime import datetime, timedelta
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def fetch_historical_finance(ticker='^GSPC', start_date='1927-12-30', resample='W'):
    """
    Fetches daily historical data and resamples to the specified frequency.
    resample='W' for Weekly, 'MS' for Monthly Start.
    """
    end_date = datetime.now().strftime('%Y-%m-%d')
    print(f"Fetching data for {ticker} from {start_date} (resample={resample})...")
    
    try:
        ticker_obj = yf.Ticker(ticker)
        raw_df = ticker_obj.history(start=start_date, end=end_date, interval='1d', auto_adjust=True)
        
        if raw_df.empty:
            raw_df = yf.download(ticker, start=start_date, end=end_date, interval='1d', progress=False)
            
        if raw_df.empty:
            return pd.DataFrame()
            
        # Extract Close Column
        if isinstance(raw_df.columns, pd.MultiIndex):
            df = raw_df['Close']
        else:
            df = raw_df[['Close']]
            
        df = pd.DataFrame(df)
        df.columns = ['Close']

        # Handle timezone
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        
        # Resample to chosen frequency
        df = df.resample(resample).last()
            
        df = df.dropna()
        print(f"DONE: Retrieved {len(df)} data points.")
        return df
        
    except Exception as e:
        print(f"Error fetching yfinance data: {e}")
        return pd.DataFrame()

def get_planet_positions(date):
    """
    Calculates geocentric longitude and speed for all key planets.
    """
    jd = swe.julday(date.year, date.month, date.day, 12.0)
    
    planets = {
        'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN,
        'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO, 'Mars': swe.MARS,
        'Mercury': swe.MERCURY, 'Sun': swe.SUN,
        'Venus': swe.VENUS, 'True_Node': swe.TRUE_NODE,
        'Moon': swe.MOON
    }
    
    features = {}
    geo_flags = swe.FLG_SPEED | swe.FLG_SWIEPH
    hel_flags = swe.FLG_SPEED | swe.FLG_SWIEPH | swe.FLG_HELCTR
    equ_flags = swe.FLG_SPEED | swe.FLG_SWIEPH | swe.FLG_EQUATORIAL # For Declination (OOB)
    
    # Planets that matter for Heliocentric cycles (The 'True Systemic Velocity')
    helio_planets = ['Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    
    for name, pid in planets.items():
        try:
            # 1. Geocentric Positions (Sentiment/Panic)
            res, _ = swe.calc_ut(jd, pid, geo_flags)
            features[f'{name}_Lon'] = res[0]
            features[f'{name}_Speed'] = res[3]
            features[f'{name}_Retro'] = 1 if res[3] < 0 else 0
            
            # 2. Declination (Equatorial) for OOB Weighting (Mars/Moon)
            if name in ['Mars', 'Moon']:
                res_equ, _ = swe.calc_ut(jd, pid, equ_flags)
                features[f'{name}_Decl'] = res_equ[1] # Declination is index 1
            
            # 3. Heliocentric Positions (Pure Orbital Gravity)
            if name in helio_planets:
                res_hel, _ = swe.calc_ut(jd, pid, hel_flags)
                features[f'{name}_Helio_Lon'] = res_hel[0]
                features[f'{name}_Helio_Speed'] = res_hel[3]
                
        except:
            return {}

    # Saturn-Neptune Angle
    if 'Saturn_Lon' in features and 'Neptune_Lon' in features:
        diff = abs(features['Saturn_Lon'] - features['Neptune_Lon'])
        if diff > 180: diff = 360 - diff
        features['Saturn_Neptune_Angle'] = diff
    
    # Moon Phase
    if 'Sun_Lon' in features and 'Moon_Lon' in features:
        features['Moon_Phase_Deg'] = (features['Moon_Lon'] - features['Sun_Lon']) % 360
        
    # Ketu
    if 'True_Node_Lon' in features:
        features['Ketu_Lon'] = (features['True_Node_Lon'] + 180) % 360
    
    return features

def build_century_master():
    print("Starting Arion.ai Ingestor - WEEKLY Century Master Build...")
    
    # 1. Fetch S&P 500 WEEKLY data
    market_df = fetch_historical_finance(resample='W')
    if market_df.empty:
        print("Aborting: No market data.")
        return

    # 2. Calculate Astro Logic for every week
    print(f"Calculating planetary positions for {len(market_df)} weeks...")
    astro_data = [get_planet_positions(d) for d in market_df.index]
    astro_df = pd.DataFrame(astro_data, index=market_df.index)
    
    # 3. Fetch VIX WEEKLY
    print("Fetching VIX weekly data...")
    vix_df = fetch_historical_finance(ticker='^VIX', start_date='1990-01-02', resample='W')
    
    # 4. Fetch Treasury Yields (Yield Curve Inversion = Recession Signal)
    print("Fetching Treasury Yields (10Y and 3M)...")
    tnx_df = fetch_historical_finance(ticker='^TNX', start_date='1990-01-02', resample='W')
    irx_df = fetch_historical_finance(ticker='^IRX', start_date='1990-01-02', resample='W')
    
    # 5. Merge Everything
    master_df = pd.concat([market_df, astro_df], axis=1)
    
    if not vix_df.empty:
        vix_df = vix_df.rename(columns={'Close': 'VIX_Close'})
        master_df = master_df.join(vix_df, how='left')
    
    if not tnx_df.empty and not irx_df.empty:
        tnx_df = tnx_df.rename(columns={'Close': 'Yield_10Y'})
        irx_df = irx_df.rename(columns={'Close': 'Yield_3M'})
        master_df = master_df.join(tnx_df, how='left')
        master_df = master_df.join(irx_df, how='left')
        # YIELD CURVE SPREAD (10Y - 3M): Negative = Inversion = Recession
        master_df['Yield_Curve_Spread'] = master_df['Yield_10Y'] - master_df['Yield_3M']
        master_df['Yield_Curve_Inverted'] = (master_df['Yield_Curve_Spread'] < 0).astype(int)
    
    # 6. Financial Engineering (WEEKLY)
    master_df['Log_Return'] = np.log(master_df['Close'] / master_df['Close'].shift(1))
    
    # Weekly Momentum (4-week and 12-week)
    master_df['Momentum_4W'] = master_df['Close'] / master_df['Close'].shift(4) - 1
    master_df['Momentum_12W'] = master_df['Close'] / master_df['Close'].shift(12) - 1
    
    # Volatility (20-week rolling StdDev of returns)
    master_df['Volatility_20W'] = master_df['Log_Return'].rolling(20).std()
    
    # Credit Stress Proxy: VIX / VIX 50-week average
    if 'VIX_Close' in master_df.columns:
        master_df['VIX_Stress_Ratio'] = master_df['VIX_Close'] / master_df['VIX_Close'].rolling(50).mean()
    
    # Target Variables (WEEKLY resolution)
    # Big Gun: Higher in 26 weeks (6 months)?
    future_26w = master_df['Close'].shift(-26) / master_df['Close'] - 1
    master_df['Target_Bullish_6M'] = (future_26w > 0).astype(int)
    
    # Sniper: Lower by 3%+ in next 12 weeks (3 months)?
    future_12w = master_df['Close'].shift(-12) / master_df['Close'] - 1
    master_df['Target_Short_Alert_3M'] = (future_12w < -0.03).astype(int)
    
    # Assault: Drop 2%+ in next 4 weeks (1 month)?
    future_4w = master_df['Close'].shift(-4) / master_df['Close'] - 1
    master_df['Target_Short_Alert_1M'] = (future_4w < -0.02).astype(int)
    
    # --- DUAL CRASH PREDATOR TARGETS ---
    # Rolling min of future 26 weeks
    rolling_min_26w = master_df['Close'].shift(-26).rolling(26, min_periods=1).min()
    
    # Target 1: Structural Collapse (-20%)
    master_df['Crash_20pct_6M'] = (rolling_min_26w / master_df['Close'] - 1 < -0.20).astype(int)
    
    # Target 2: Correction (-10%)
    master_df['Crash_10pct_6M'] = (rolling_min_26w / master_df['Close'] - 1 < -0.10).astype(int)
    
    # Target 3: Micro-Pulse (-5%) - HIGH RESOLUTION SENSITIVITY
    master_df['Crash_5pct_6M'] = (rolling_min_26w / master_df['Close'] - 1 < -0.05).astype(int)

    # --- SOVEREIGN DASHA INTEGRATION (S&P 500 Natal: Mar 4, 1957) ---
    print("Calculating S&P 500 Natal Dasha periods...")
    dasha_engine = VimshottariDasha()
    # S&P Standard Natal Source: Mar 4, 1957. Moon approx: Revati (Ketu/Saturn influence)
    # Estimated Moon Lon for 1957-03-04: ~348 (Revati)
    natal_moon = 348.0 
    birth_dt = datetime(1957, 3, 4)
    
    dashas = []
    for d in master_df.index:
        d_info = dasha_engine.get_current_dasha(natal_moon, birth_dt, d.to_pydatetime())
        dashas.append({
            'Mahadasha': d_info['Mahadasha'],
            'Antardasha': d_info['Antardasha']
        })
    dasha_df = pd.DataFrame(dashas, index=master_df.index)
    master_df = pd.concat([master_df, dasha_df], axis=1)

    # Max Drawdown in next 12 weeks
    master_df['Max_Drift_3M'] = master_df['Close'].rolling(12).min().shift(-12) / master_df['Close'] - 1
    
    # 7. Save
    os.makedirs(os.path.join('data', 'raw'), exist_ok=True)
    output_path = os.path.join('data', 'raw', 'century_master.csv')
    master_df.to_csv(output_path)
    
    print("\n" + "="*50)
    print("WEEKLY CENTURY MASTER DATASET GENERATED")
    print("="*50)
    print(f"Total Rows: {len(master_df)} (vs ~1180 monthly before)")
    print(f"Columns: {len(master_df.columns)}")
    print(f"Dataset saved to: {output_path}")

if __name__ == "__main__":
    build_century_master()
