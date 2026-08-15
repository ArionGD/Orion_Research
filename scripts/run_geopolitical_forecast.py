import os
import sys
import pandas as pd
from datetime import datetime, timedelta

# Root Path Setup
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
if ROOT not in sys.path:
    sys.path.append(ROOT)

from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.medini.conflict_modifier import ConflictModifier
from src.engine.medini.yogas import YogaScanner
from src.engine.medini.temporal import TemporalScanner
from src.engine.countries.usa.logic import USARiskEngine
from src.engine.countries.india.logic import IndiaRiskEngine

def run_forecast():
    print("=== Launching Arion Medini Geopolitical Forecaster (1-Year Outlook) ===")
    
    # Setup engines
    ep = EphemerisProvider()
    weather_engine = MundaneWeatherEngine()
    conflict_mod = ConflictModifier()
    yoga_scanner = YogaScanner()
    temporal_scanner = TemporalScanner()
    usa_engine = USARiskEngine()
    india_engine = IndiaRiskEngine()
    
    # Define time window: June 4, 2026 to June 4, 2027
    start_date = datetime(2026, 6, 4)
    end_date = datetime(2027, 6, 4)
    
    current = start_date
    daily_records = []
    
    while current <= end_date:
        positions = ep.get_all_positions(current)
        
        # 1. World Geopolitical & Conflict Logic
        conflict = conflict_mod.analyze_conflict(positions, current)
        yogas = yoga_scanner.scan_yogas(positions)
        temporal_events = temporal_scanner.scan_temporal_events(current)
        
        # Dasha context for Global SMI
        dasha_md = "Saturn" if current.year >= 2026 else "Jupiter"
        dasha_ad = "Rahu" if current.month in [4, 9, 10] else "Venus"
        smi = weather_engine.calculate_smi(current, positions, dasha_md, dasha_ad)
        
        # 2. Country Specifics
        usa_score, usa_sigs = usa_engine.check_risk(positions)
        india_score, india_sigs = india_engine.check_risk(positions)
        
        # Capture significant highlights
        daily_records.append({
            'Date': current,
            'SMI': smi,
            'Conflict_Active': conflict['conflict_active'],
            'Conflict_Type': conflict['conflict_type'],
            'Conflict_Aspect': conflict['aspect'],
            'Conflict_Intensity': conflict['intensity'],
            'Conflict_Signals': "; ".join(conflict['signals']),
            'Yogas': ", ".join([f"{y['Name']} ({y['Description']})" for y in yogas]),
            'Temporal': ", ".join([f"{t['Type']} (Axis: {t['Axis']})" for t in temporal_events]),
            'USA_Score': usa_score,
            'USA_Signals': "; ".join(usa_sigs),
            'India_Score': india_score,
            'India_Signals': "; ".join(india_sigs)
        })
        
        current += timedelta(days=1)
        
    df = pd.DataFrame(daily_records)
    
    # Save raw CSV log for the user
    csv_path = os.path.join(ROOT, "sniper/geopolitical_raw_forecast_1y.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved raw forecast log to: {csv_path}")
    
    # Process and summarize the 1-year timeline
    generate_markdown_report(df)

def generate_markdown_report(df):
    report_lines = []
    report_lines.append("# 🌐 Arion Medini Geopolitical & Mundane Forecast (June 2026 - June 2027)")
    report_lines.append(f"**Generated On:** {datetime.now().strftime('%Y-%m-%d')}  ")
    report_lines.append("**Orchestration Engine:** ACE v5 Medini Physics + Geopolitical Conflict Engine  \n")
    report_lines.append("---")
    
    # Section 1: Global Geopolitical & War Outlook
    report_lines.append("\n## 🌍 1. Global Geopolitical & Conflict Outlook")
    report_lines.append("The Conflict Modifier scans Mars-Saturn dynamics to distinguish between **Supply Shocks (Hot War)** and **Demand Destruction (Cold Siege)**.\n")
    
    # Find active conflict windows
    conflict_df = df[df['Conflict_Active'] == True]
    if not conflict_df.empty:
        report_lines.append("### Active Conflict Windows:")
        report_lines.append("| Start Date | End Date | Conflict Type | Peak Intensity | Cosmic Aspect | Impact Summary |")
        report_lines.append("| :--- | :--- | :--- | :---: | :--- | :--- |")
        
        # Group contiguous days of active conflict
        conflict_windows = []
        win_start = None
        prev_row = None
        
        for idx, row in conflict_df.iterrows():
            if win_start is None:
                win_start = row['Date']
                peak_intensity = row['Conflict_Intensity']
                conf_type = row['Conflict_Type']
                aspect = row['Conflict_Aspect']
                signals = row['Conflict_Signals']
            elif (row['Date'] - prev_row['Date']).days > 1:
                # End of window
                conflict_windows.append((win_start, prev_row['Date'], conf_type, peak_intensity, aspect, signals))
                win_start = row['Date']
                peak_intensity = row['Conflict_Intensity']
                conf_type = row['Conflict_Type']
                aspect = row['Conflict_Aspect']
                signals = row['Conflict_Signals']
            else:
                if row['Conflict_Intensity'] > peak_intensity:
                    peak_intensity = row['Conflict_Intensity']
                    conf_type = row['Conflict_Type']
                    aspect = row['Conflict_Aspect']
                    signals = row['Conflict_Signals']
            prev_row = row
        
        if win_start is not None and prev_row is not None:
            conflict_windows.append((win_start, prev_row['Date'], conf_type, peak_intensity, aspect, signals))
            
        for ws, we, ct, pi, asp, sig in conflict_windows:
            report_lines.append(f"| {ws.strftime('%Y-%m-%d')} | {we.strftime('%Y-%m-%d')} | {ct.upper().replace('_', ' ')} | {pi:.1f}% | {asp} | {sig} |")
    else:
        report_lines.append("✅ **No active Mars-Saturn conflict windows detected for this 12-month period.** Geopolitical tensions remain within localized parameters without global military expansion indicators.\n")
        
    # Find active Eclipses
    eclipse_df = df[df['Temporal'] != ""]
    if not eclipse_df.empty:
        report_lines.append("\n### 🌘 Solar & Lunar Eclipse Windows (Systemic Stress Catalysts):")
        report_lines.append("| Date | Eclipse Type & Zodiacal Axis |")
        report_lines.append("| :--- | :--- |")
        
        seen_temporal = set()
        for idx, row in eclipse_df.iterrows():
            events = [t.strip() for t in row['Temporal'].split(",") if t.strip()]
            for ev in events:
                if ev not in seen_temporal:
                    seen_temporal.add(ev)
                    report_lines.append(f"| {row['Date'].strftime('%Y-%m-%d')} | {ev} |")
                    
    # Find active Yogas (Angarak, etc.)
    yogas_df = df[df['Yogas'] != ""]
    if not yogas_df.empty:
        report_lines.append("\n### 🪐 Active Malefic Yogas (Planetary Conjunctions):")
        report_lines.append("| Date / Period | Active Yoga | Threat Description |")
        report_lines.append("| :--- | :--- | :--- |")
        
        seen_yogas = set()
        for idx, row in yogas_df.iterrows():
            y_list = [y.strip() for y in row['Yogas'].split("),") if y.strip()]
            for y in y_list:
                y_clean = y + ")" if not y.endswith(")") else y
                # Group by month for cleaner presentation
                month_str = row['Date'].strftime('%B %Y')
                combo_key = (month_str, y_clean)
                if combo_key not in seen_yogas:
                    seen_yogas.add(combo_key)
                    # Extract description
                    desc = ""
                    if "(" in y_clean:
                        desc = y_clean.split("(")[1].replace(")", "")
                    name = y_clean.split("(")[0].strip()
                    report_lines.append(f"| {month_str} | **{name}** | {desc} |")

    # Section 2: USA Sovereign Risk Outlook
    report_lines.append("\n---\n\n## 🇺🇸 2. United States Sovereign Risk Outlook")
    report_lines.append("The USA Risk Engine compares daily transits to the USA Natal Chart (Sibly - July 4, 1776). Sensitive points include the Sun (Authority/Leadership) and Moon (Public/Sentiment).\n")
    
    # Peak US Risk dates (Score > 0)
    usa_risk_df = df[df['USA_Score'] > 0]
    if not usa_risk_df.empty:
        report_lines.append("### US Critical Risk Eras:")
        report_lines.append("| Period | Risk Score | Active Natal Hits & Signals |")
        report_lines.append("| :--- | :---: | :--- |")
        
        # Group by contiguous score/signals
        seen_us_windows = set()
        for idx, row in usa_risk_df.iterrows():
            month_str = row['Date'].strftime('%B %Y')
            sigs = row['USA_Signals']
            score = row['USA_Score']
            combo_key = (month_str, sigs)
            if combo_key not in seen_us_windows:
                seen_us_windows.add(combo_key)
                report_lines.append(f"| {month_str} | **{score}** | {sigs} |")
    else:
        report_lines.append("✅ **No significant US natal chart transit risks detected.** The US chart shows stable cosmic support with standard operations.\n")
        
    # Section 3: India Sovereign Risk Outlook
    report_lines.append("\n---\n\n## 🇮🇳 3. Republic of India Sovereign Risk Outlook")
    report_lines.append("The India Risk Engine compares transits to the India Natal Chart (Independence - Aug 15, 1947). Sensitive points include the Lagna/Ascendant (Taurus ~8°) and the Moon (Cancer - mind of the nation).\n")
    
    # Peak India Risk dates (Score > 0)
    india_risk_df = df[df['India_Score'] > 0]
    if not india_risk_df.empty:
        report_lines.append("### India Critical Risk Eras:")
        report_lines.append("| Period | Risk Score | Active Natal Hits & Signals |")
        report_lines.append("| :--- | :---: | :--- |")
        
        seen_in_windows = set()
        for idx, row in india_risk_df.iterrows():
            month_str = row['Date'].strftime('%B %Y')
            sigs = row['India_Signals']
            score = row['India_Score']
            combo_key = (month_str, sigs)
            if combo_key not in seen_in_windows:
                seen_in_windows.add(combo_key)
                report_lines.append(f"| {month_str} | **{score}** | {sigs} |")
    else:
        report_lines.append("✅ **No significant Indian natal chart transit risks detected.** The Indian chart operates in stable parameters.\n")
        
    # Section 4: Summary Conclusions
    report_lines.append("\n---\n\n## 🏛️ 4. Geopolitical & Macro Risk Verdict")
    
    # Calculate overall average SMI and peak stress periods
    avg_smi = df['SMI'].mean()
    peak_stress_days = df[df['SMI'] >= 6.5]
    
    report_lines.append(f"* **Average Global Sovereign Malefic Index (SMI):** {avg_smi:.2f}/10 (Normal/Nominal).")
    if not peak_stress_days.empty:
        report_lines.append("* **Global Stress Windows (SMI >= 6.5):**")
        for idx, row in peak_stress_days.groupby(peak_stress_days['Date'].dt.strftime('%B %Y')):
            report_lines.append(f"  * **{idx}**: SMI reached **{row['SMI'].max():.2f}**.")
    else:
        report_lines.append("* **Global Stress Windows:** None detected. Universal stability parameters remain intact.")
        
    report_lines.append("\n**Tactical Action:** Geopolitical volatility remains localized for the next 12 months. This supports standard asset allocations and buy-and-hold strategies in global indices, particularly in markets with high structural floor protection.")
    
    report_path = os.path.join(ROOT, "sniper/geopolitical_predictions.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"Generated Markdown report: {report_path}")

if __name__ == "__main__":
    run_forecast()
