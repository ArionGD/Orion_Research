import pandas as pd
import os
import re

class ArionTranslator:
    def __init__(self):
        self.features_path = 'data/processed/refined_features.csv'
        self.prophecy_path = 'data/processed/prophecy_2026_2030.csv'
        self.sentinel_path = 'src/alerts/SENTINEL_FEB_2026.md'
        
        self.term_map = {
            'Global_Stability_Index': 'Structural System Pressure',
            'Havoc_Score': 'Systemic Instability Probability',
            'Flash_Crash_Probability': 'Sudden Liquidity Withdrawal Risk',
            'Mars_Volatility_Score': 'Kinetic Conflict Index',
            'Uranus_Station': 'Network/Regulatory Gridlock'
        }

    def load_features(self, date):
        # 1. Try Refined Features (History)
        if os.path.exists(self.features_path):
            df = pd.read_csv(self.features_path, parse_dates=['Date'], index_col='Date')
            # Check if date is in index (exact or month match)
            # using nearest for now, but strictly we want the specific month if possible
            if date in df.index:
                return df.loc[date]
            
            # If date < max date in refined, use nearest
            if not df.empty and date <= df.index.max():
                 idx = df.index.get_indexer([pd.Timestamp(date)], method='nearest')[0]
                 return df.iloc[idx]

        # 2. Try Prophecy (Future)
        if os.path.exists(self.prophecy_path):
            df_p = pd.read_csv(self.prophecy_path, parse_dates=['Date'], index_col='Date')
            if date in df_p.index:
                return df_p.loc[date]
            # If date is within prophecy range
            if not df_p.empty and date >= df_p.index.min():
                idx = df_p.index.get_indexer([pd.Timestamp(date)], method='nearest')[0]
                return df_p.iloc[idx]
        
        return None

    def _read_sentinel_score(self, date_str):
        # Scan markdown for date string YYYY-MM-DD
        if not os.path.exists(self.sentinel_path):
            return 0.0
            
        with open(self.sentinel_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Pattern: ### ⚠️ 2026-02-01 (Risk Score: 9.5/10)
        pattern = f"### .*? {date_str} \\(Risk Score: ([\\d\\.]+)/10\\)"
        match = re.search(pattern, content)
        if match:
            return float(match.group(1))
        return 0.0

    def generate_executive_report(self, date):
        date_str = date.strftime('%Y-%m-%d')
        feats = self.load_features(date)
        sentinel_score = self._read_sentinel_score(date_str)
        
        if feats is None:
            return "Data unavailable for executive summary."

        # Extract Metrics
        flash_prob = feats.get('Flash_Crash_Probability', 0)
        gsi = feats.get('Global_Stability_Index', 1000)
        
        # Translation Logic
        
        # Header
        report = f"## 📑 ARION EXECUTIVE MEMO: {date_str}\n\n"
        
        # Paragraph 1: Status
        confidence = max(sentinel_score, flash_prob * 10) # Normalize flash to 0-10
        status = "NORMAL"
        if confidence > 5: status = "ELEVATED"
        if confidence > 8: status = "CRITICAL"
        
        report += f"**SUBJECT: MARKET RISK ASSESSMENT - {status}**\n\n"
        
        report += f"**1. SITUATION REPORT:**\n"
        report += f"Current models indicate a Risk Confidence Level of **{confidence:.1f}/10**. "
        if status == "CRITICAL":
            report += "We are currently in a **CRITICAL ALERT** status. "
        report += "The system has detected valid precursors for a significant liquidity event. \n\n"
        
        # Paragraph 2: The "Why" (Translated)
        report += f"**2. STRUCTURAL ANALYSIS:**\n"
        
        drivers = []
        if sentinel_score > 8:
            drivers.append("Major Structural Re-alignment in Global Banking Systems (NYSE Core Pressure)")
        if flash_prob > 0.4:
            drivers.append("High probability of Sudden Liquidity Withdrawal (Flash Crash Risk)")
        if gsi < 800:
             drivers.append("Extreme Structural System Pressure (The 'walls are closing in')")
             
        if not drivers:
            report += "Global systems are operating within nominal parameters. No immediate structural threats detected.\n\n"
        else:
            report += "Primary drivers include: " + "; ".join(drivers) + ". "
            report += "Technological and regulatory gridlock may cause sudden freezes in capital flows.\n\n"
            
        # Paragraph 3: Actionable Insights
        report += f"**3. STRATEGIC IMPLICATIONS:**\n"
        actions = []
        if status == "CRITICAL":
            actions.append("Ensure high cash-on-hand positions immediately")
            actions.append("Monitor tech-sector stops and high-frequency trading halts")
            actions.append("Prepare for potential exchange outages")
        elif status == "ELEVATED":
            actions.append("Reduce leverage in speculative assets")
            actions.append("Tighten stop-loss perimeters")
        else:
            actions.append("Maintain standard accumulating positions")
            actions.append("Monitor peripheral volatility")
            
        report += "Recommended posture: " + "; ".join(actions) + "."
        
        return report



    def generate_sector_ratings(self, features):
        """
        Generates detailed industry risk ratings based on astro-metrics.
        Input: features (pd.Series)
        Output: pd.DataFrame with columns: Rank, Sector, Industry, Score, Rating, Status, Color
        """
        if features is None:
            return pd.DataFrame()

        # 1. Define Hierarchy and Base Scores (50 = Neutral, >60 Safe, <40 Risky)
        # Hierarchy: Sector -> {Industry: BaseScore}
        hierarchy = {
            'Financials': {
                'Major Banks': 50,
                'Regional Banking': 45,
                'Insurance': 60,
                'Capital Markets': 45,
                'Fintech & Payments': 40
            },
            'Technology': {
                'Software & AI': 45,
                'Semiconductors': 40,
                'Hardware': 45,
                'Cybersecurity': 55
            },
            'Industrials': {
                'Aerospace & Defense': 60,
                'Construction & Engineering': 50,
                'Logistics & Transport': 45,
                'Machinery': 50
            },
            'Energy': {
                'Oil & Gas E&P': 50,
                'Oil Services': 45,
                'Renewable Energy': 45
            },
            'Healthcare': {
                'Pharmaceuticals': 60,
                'Biotech': 45,
                'Providers & Services': 65,
                'MedTech': 55
            },
            'Consumer Discretionary': {
                'Automobiles': 40,
                'Luxury Goods': 45,
                'Hotels & Leisure': 40,
                'Retail (Non-Essential)': 45
            },
            'Consumer Staples': {
                'Food & Beverage': 65,
                'Household Prdcts': 65,
                'Tobacco/Alcohol': 60
            },
            'Utilities': {
                'Electric Utilities': 70,
                'Water Utilities': 70,
                'Gas Utilities': 65
            },
            'Real Estate': {
                'Residential REITs': 50,
                'Commercial/Office': 40,
                'Industrial REITs': 55
            },
            'Communication': {
                'Media & Entertainment': 45,
                'Telecom Services': 55,
                'Social Media': 40
            },
            'Materials': {
                'Metals & Mining': 45,
                'Chemicals': 50,
                'Gold/Precious Metals': 65 # Often hedge
            }
        }

        # --- ASTRO MODIFIERS ---
        
        # 1. Mars Volatility (Conflict/Aggression)
        # Boosts Defense, Energy, Cyber. Hurts Cons Disc, Travel, Tech (High beta).
        mars_vol = features.get('Mars_Volatility_Score', 0)
        mars_impact = 0
        if mars_vol > 0.5: mars_impact = 1
        if mars_vol > 0.8: mars_impact = 2

        if mars_impact > 0:
            penalty = 10 * mars_impact
            boost = 10 * mars_impact
            
            # Hurts
            hierarchy['Technology']['Software & AI'] -= penalty
            hierarchy['Technology']['Semiconductors'] -= penalty
            hierarchy['Consumer Discretionary']['Hotels & Leisure'] -= penalty
            hierarchy['Consumer Discretionary']['Automobiles'] -= penalty
            hierarchy['Communication']['Social Media'] -= penalty
            
            # Boosts (Hedges)
            hierarchy['Industrials']['Aerospace & Defense'] += boost
            hierarchy['Technology']['Cybersecurity'] += boost
            hierarchy['Materials']['Gold/Precious Metals'] += (boost * 0.5)
            hierarchy['Energy']['Oil & Gas E&P'] += (boost * 0.5)

        # 2. Global Stability Index (Systemic Stress)
        # Low GSI = Credit crunch. Kills Financials, RE, Cyclicals.
        gsi = features.get('Global_Stability_Index', 1000)
        if gsi < 850:
            stress_penalty = 20
            if gsi < 700: stress_penalty = 30
            
            for k in hierarchy['Financials']: hierarchy['Financials'][k] -= stress_penalty
            for k in hierarchy['Real Estate']: hierarchy['Real Estate'][k] -= stress_penalty
            hierarchy['Industrials']['Construction & Engineering'] -= (stress_penalty * 0.8)
            hierarchy['Consumer Discretionary']['Luxury Goods'] -= stress_penalty
            
            # Flight to Safety
            hierarchy['Utilities']['Electric Utilities'] += 15
            hierarchy['Consumer Staples']['Food & Beverage'] += 15
            hierarchy['Healthcare']['Pharmaceuticals'] += 10
            hierarchy['Materials']['Gold/Precious Metals'] += 20

        # 3. Saturn-Neptune (Dissolution, Confusion, Poison, Water)
        # Hurts Oil (Fluids), Pharma (Scandal), Media (Deception), Maritime. 
        # Often deflationary -> Hurts Commodities.
        sn_angle = features.get('Saturn_Neptune_Angle', None)
        if sn_angle is not None:
             # Check approx 0, 90, 180
             is_hard_sn = (sn_angle < 15) or (80 < sn_angle < 100) or (170 < sn_angle < 190) or (sn_angle > 345)
             
             if is_hard_sn:
                 hierarchy['Energy']['Oil & Gas E&P'] -= 15
                 hierarchy['Energy']['Oil Services'] -= 15
                 hierarchy['Materials']['Chemicals'] -= 15
                 hierarchy['Healthcare']['Pharmaceuticals'] -= 10 # Complexity/Scandal risk
                 hierarchy['Industrials']['Logistics & Transport'] -= 10 # Shipping disruptions
                 hierarchy['Communication']['Media & Entertainment'] -= 10 # Trust issues

        # 4. Flash Crash (Liquidity Shock)
        flash_prob = features.get('Flash_Crash_Probability', features.get('Havoc_Score', 0))
        if flash_prob > 0.45:
            # Broad market selloff risk -> Cash is king.
            # Reduce everything except hyper-defensive
            for sector, inds in hierarchy.items():
                for ind in inds:
                    hierarchy[sector][ind] -= 15
            
            # Restore Defensives slightly (relative strength)
            hierarchy['Utilities']['Electric Utilities'] += 10
            hierarchy['Consumer Staples']['Household Prdcts'] += 10
            hierarchy['Materials']['Gold/Precious Metals'] += 10

        # Construct DataFrame
        rows = []
        for sector, industries in hierarchy.items():
            for industry, score in industries.items():
                
                # Cap scores 0-100
                score = max(0, min(100, score))
                
                # Extended Volatility Spectrum (6 Tiers)
                if score >= 75:
                    rating = "Fortress (AAA)"
                    status = "Maximal Safety"
                    color = "#00FF00" # Deep Neon Green
                    tier = 1
                elif score >= 65:
                    rating = "Accumulate (AA)"
                    status = "Resilient"
                    color = "#90EE90" # Light Green
                    tier = 2
                elif score >= 55:
                    rating = "Neutral (A)"
                    status = "Stable"
                    color = "#FFFF00" # Yellow
                    tier = 3
                elif score >= 45:
                    rating = "Speculative (BBB)"
                    status = "Volatile"
                    color = "#FFA500" # Orange
                    tier = 4
                elif score >= 35:
                    rating = "Underperform (BB)"
                    status = "High Risk"
                    color = "#FF4500" # Red-Orange
                    tier = 5
                else:
                    rating = "SHORT (CCC)"
                    status = "Crash Vulnerable"
                    color = "#FF0000" # Deep Red
                    tier = 6
                
                rows.append({
                    'Sector': sector,
                    'Industry': industry,
                    'Score': int(score),
                    'Rating': rating,
                    'Status': status,
                    'Color': color,
                    'Tier': tier
                })

        df = pd.DataFrame(rows).sort_values(by='Score', ascending=False).reset_index(drop=True)
        df.index += 1
        df['Rank'] = df.index
        
        return df[['Rank', 'Sector', 'Industry', 'Score', 'Rating', 'Status', 'Color', 'Tier']]

if __name__ == "__main__":
    translator = ArionTranslator()
    # Test Feb 4 2026
    print(translator.generate_executive_report(pd.Timestamp('2026-02-04')))
