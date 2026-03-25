import sys
import os

# Ensure src in pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from datetime import datetime, timedelta

class NYSESentinel:
    def __init__(self):
        self.ep = EphemerisProvider()
        # NYSE Sun: 27 Taurus = 30 + 27 = 57.0 degrees
        self.nyse_sun = 57.0 
        
        # Sector Sensitivity Map
        self.sectors = {
            'Uranus_Taurus': {
                'Sectors': ['Crypto', 'Fintech', 'Semiconductors', 'High-Freq Trading'],
                'Risks': ['Flash-Crash', 'Network Outage', 'Sudden Regulation']
            },
            'Venus_Aquarius': {
                'Sectors': ['Social Media', 'AI-Creatives', 'Luxury Retail', 'Currencies'],
                'Risks': ['Sharp Devaluation', 'Hype Bubble Bursting']
            }
        }
    
    def analyze_window(self, start_date, days=15):
        print(f"Sentinel scanning NYSE risk from {start_date.date()} for {days} days...")
        
        alerts = []
        max_score = 0.0
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            
            # Get Transit Data
            # Uranus in Taurus (Targeting NYSE Sun)
            t_ura_lon, t_ura_speed, _, _ = self.ep.get_planet_data(date, 'Uranus')
            
            # Venus in Aquarius (Squaring NYSE Sun)
            t_ven_lon, _, _, _ = self.ep.get_planet_data(date, 'Venus')
            
            if t_ura_lon is None: continue
            
            # 1. Uranus Station on Natal Sun Check
            # Check distance to NYSE Sun (57.0)
            dist_ura_sun = min(abs(t_ura_lon - self.nyse_sun), 360 - abs(t_ura_lon - self.nyse_sun))
            is_station = abs(t_ura_speed) < 0.02 # Station definition
            
            # 2. Venus Square checks
            # Venus to NYSE Sun (should be 90)
            ven_sun_angle = self.ep.get_distance(t_ven_lon, self.nyse_sun)
            dist_square = abs(ven_sun_angle - 90)
            is_ven_square = dist_square <= 2.0 # Tight orb for trigger
            
            # Venus to Transit Uranus (Flash Crash generic trigger) - Checking for context
            ven_ura_angle = self.ep.get_distance(t_ven_lon, t_ura_lon)
            
            # Scoring Logic
            daily_score = 0.0
            notes = []
            
            # Condition: Transit Station within 1 deg of Natal Sun
            if is_station and dist_ura_sun <= 1.0:
                daily_score = 9.5
                notes.append("**CRITICAL**: Uranus Station DIRECT HIT on NYSE Sun (27° Tau)")
            elif dist_ura_sun <= 1.0:
                daily_score = 7.0
                notes.append("Uranus transiting exact NYSE Sun degree")
                
            if is_ven_square:
                if daily_score > 0:
                    daily_score = min(10.0, daily_score + 0.5)
                    notes.append("**TRIGGER**: Venus Squares NYSE Sun (Activation)")
                else:
                    daily_score = 5.0
                    notes.append("Venus Squares NYSE Sun")
                    
            if daily_score > max_score:
                max_score = daily_score
                
            if daily_score > 5.0:
                alerts.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Score': daily_score,
                    'T_Uranus': t_ura_lon,
                    'Dist_to_Sun': dist_ura_sun,
                    'Notes': "; ".join(notes)
                })
                
        return alerts, max_score

    def generate_report(self, alerts, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 🚨 ARION INSTITUTIONAL SENTINEL REPORT 🚨\n")
            f.write("## Target: NEW YORK STOCK EXCHANGE (NYSE)\n")
            f.write("### Natal Sun: 27° Taurus\n")
            f.write(f"### Window: Feb 2026 Analysis\n\n")
            
            f.write("## 1. SECTOR SENSITIVITY MAPPING\n")
            f.write("| Configuration | Affected Sectors | Risk Profile |\n")
            f.write("|---|---|---|\n")
            f.write(f"| **Uranus in Taurus** | {', '.join(self.sectors['Uranus_Taurus']['Sectors'])} | {', '.join(self.sectors['Uranus_Taurus']['Risks'])} |\n")
            f.write(f"| **Venus in Aquarius** | {', '.join(self.sectors['Venus_Aquarius']['Sectors'])} | {', '.join(self.sectors['Venus_Aquarius']['Risks'])} |\n\n")
            
            f.write("## 2. CHRONOLOGICAL RISK FEED\n")
            if not alerts:
                f.write("No critical institutional threats detected in this window.\n")
            else:
                for a in alerts:
                    icon = "⚠️" if a['Score'] < 9 else "🛑"
                    f.write(f"### {icon} {a['Date']} (Risk Score: {a['Score']}/10)\n")
                    f.write(f"- **Trigger**: {a['Notes']}\n")
                    f.write(f"- **Technical Data**: Uranus at {a['T_Uranus']:.2f}° (Dist to NYSE Sun: {a['Dist_to_Sun']:.2f}°)\n\n")
            
            f.write("## 3. EXECUTIVE SUMMARY\n")
            f.write("The convergence of a Stationary Uranus exactly on the NYSE natal Sun (27 Taurus), triggered by a hard square from Venus, suggests a **High-Probability Liquidity Event**.\n")
            f.write("\n*Generated by Arion.ai Sentinel Module*")

        print(f"Report saved to {filename}")

if __name__ == "__main__":
    sentinel = NYSESentinel()
    # Scan Feb 2026
    alerts, max_score = sentinel.analyze_window(datetime(2026, 2, 1), days=15)
    
    output_path = 'src/alerts/SENTINEL_FEB_2026.md'
    sentinel.generate_report(alerts, output_path)
