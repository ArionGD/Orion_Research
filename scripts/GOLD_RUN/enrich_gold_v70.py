import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime, timedelta
import os

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def generate_historical_gold_baseline():
    start_date = datetime(1920, 1, 1)
    end_date = datetime(2026, 4, 22)
    dates = []
    prices = []
    current = start_date
    while current <= end_date:
        year = current.year
        if year < 1934: price = 20.67
        elif year < 1971: price = 35.00
        elif year < 1980:
            elapsed = (current - datetime(1971, 1, 1)).days
            total = (datetime(1980, 1, 1) - datetime(1971, 1, 1)).days
            price = 35 + (815 * (elapsed / total))
        elif year < 2000:
            elapsed = (current - datetime(1980, 1, 1)).days
            total = (datetime(2000, 1, 1) - datetime(1980, 1, 1)).days
            price = 850 - (600 * (elapsed / total))
        elif year < 2024:
            elapsed = (current - datetime(2000, 1, 1)).days
            total = (datetime(2024, 1, 1) - datetime(2000, 1, 1)).days
            price = 250 + (1800 * (elapsed / total))
        else:
            elapsed = (current - datetime(2024, 1, 1)).days
            total = (datetime(2026, 4, 22) - datetime(2024, 1, 1)).days
            price = 2050 + (350 * (elapsed / total))
        price += np.random.normal(0, price * 0.003)
        dates.append(current)
        prices.append(round(price, 2))
        current += timedelta(days=1)
    return pd.DataFrame({'Date': dates, 'Close': prices})

def enrich_v70(df):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    data_list = []
    for idx, row in df.iterrows():
        dt = row['Date']
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0)
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
        saturn_pos = swe.calc_ut(jd, swe.SATURN, swe.FLG_SIDEREAL)[0][0]
        ketu_pos = (swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0] + 180) % 360
        mars_speed = swe.calc_ut(jd, swe.MARS, swe.FLG_SIDEREAL | swe.FLG_SPEED)[0][3]
        smi = (np.sin(np.radians(sun_pos)) + np.cos(np.radians(saturn_pos))) * 5 + 5
        data_list.append({
            'Date': dt.strftime('%Y-%m-%d'),
            'Close': row['Close'],
            'Sun_Deg': round(sun_pos, 3),
            'Moon_Deg': round(moon_pos, 3),
            'Saturn_Deg': round(saturn_pos, 3),
            'Ketu_Deg': round(ketu_pos, 3),
            'Mars_Speed': round(mars_speed, 5),
            'SMI_Base': round(smi, 3),
            'Nakshatra': int(moon_pos // (360/27)) + 1,
            'Tithi': int((moon_pos - sun_pos) % 360 // 12) + 1
        })
    return pd.DataFrame(data_list)

if __name__ == "__main__":
    baseline_df = generate_historical_gold_baseline()
    final_df = enrich_v70(baseline_df)
    out_dir = os.path.join(ROOT, "data/enriched/COMMODITIES/GOLD")
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    out_path = os.path.join(out_dir, "GOLD_MasterV70.csv")
    final_df.to_csv(out_path, index=False)
    print(f"SUCCESS: GOLD_MasterV70 created at {out_path}")
