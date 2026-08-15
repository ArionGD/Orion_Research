"""
Corporate Astrology & Dual Risk Engine
Combines Company Natal Horoscopes (Incorporation Date/Time) with Mundane SMI Weather
and VedAstro Engine to calculate Dual Alignment Disaster & Growth Scores for NSE Stocks & Indices.
"""
from datetime import datetime
import swisseph as swe
from src.engine.astro.core.ephemeris_provider import EphemerisProvider

PRESET_COMPANIES = {
    # 📈 1. Indices & ETFs
    "NIFTY50": {"name": "Nifty 50 Index", "date": "1996-04-22", "city": "Mumbai, India", "category": "Indices & ETFs", "sector": "Benchmark"},
    "NIFTYNEXT50": {"name": "Nifty Next 50 Index", "date": "1996-12-24", "city": "Mumbai, India", "category": "Indices & ETFs", "sector": "Large Cap"},
    "NIFTYMIDCAP100": {"name": "Nifty Midcap 100 Index", "date": "2001-01-01", "city": "Mumbai, India", "category": "Indices & ETFs", "sector": "Mid Cap"},
    "NIFTYSMALLCAP100": {"name": "Nifty Smallcap 100 Index", "date": "2004-01-01", "city": "Mumbai, India", "category": "Indices & ETFs", "sector": "Small Cap"},
    "BANKNIFTY": {"name": "Bank Nifty Index", "date": "2000-01-01", "city": "Mumbai, India", "category": "Indices & ETFs", "sector": "Banking"},
    "NIFTYIT": {"name": "Nifty IT Index", "date": "1996-01-01", "city": "Mumbai, India", "category": "Indices & ETFs", "sector": "Technology"},
    "GOLDBEES": {"name": "Nippon India Gold ETF", "date": "2007-03-08", "city": "Mumbai, India", "category": "Indices & ETFs", "sector": "Metals"},
    "SILVERBEES": {"name": "Nippon India Silver ETF", "date": "2022-02-02", "city": "Mumbai, India", "category": "Indices & ETFs", "sector": "Metals"},

    # 🏦 2. BFSI (Banking & Financial Services)
    "HDFCBANK": {"name": "HDFC Bank Ltd", "date": "1994-08-30", "city": "Mumbai, India", "category": "BFSI", "sector": "Banking"},
    "ICICIBANK": {"name": "ICICI Bank Ltd", "date": "1994-01-05", "city": "Vadodara, India", "category": "BFSI", "sector": "Banking"},
    "SBIN": {"name": "State Bank of India", "date": "1955-07-01", "city": "Mumbai, India", "category": "BFSI", "sector": "Banking"},
    "BAJFINANCE": {"name": "Bajaj Finance Ltd", "date": "1987-03-25", "city": "Pune, India", "category": "BFSI", "sector": "Financial Services"},

    # 💻 3. IT (Information Technology)
    "TCS": {"name": "Tata Consultancy Services Ltd", "date": "1968-04-01", "city": "Mumbai, India", "category": "IT", "sector": "Technology"},
    "INFY": {"name": "Infosys Limited", "date": "1981-07-02", "city": "Pune, India", "category": "IT", "sector": "Technology"},
    "WIPRO": {"name": "Wipro Limited", "date": "1945-12-29", "city": "Amalner, India", "category": "IT", "sector": "Technology"},
    "TECHM": {"name": "Tech Mahindra Ltd", "date": "1986-10-24", "city": "Pune, India", "category": "IT", "sector": "Technology"},

    # ⚡ 4. Energy, Oil & Power
    "RELIANCE": {"name": "Reliance Industries Ltd", "date": "1973-05-08", "city": "Mumbai, India", "category": "Energy & Power", "sector": "Energy"},
    "ONGC": {"name": "Oil & Natural Gas Corp Ltd", "date": "1956-08-14", "city": "Dehradun, India", "category": "Energy & Power", "sector": "Energy"},
    "BPCL": {"name": "Bharat Petroleum Corp Ltd", "date": "1952-01-24", "city": "Mumbai, India", "category": "Energy & Power", "sector": "Energy"},
    "NTPC": {"name": "NTPC Limited", "date": "1975-11-07", "city": "New Delhi, India", "category": "Energy & Power", "sector": "Power"},
    "POWERGRID": {"name": "Power Grid Corp of India", "date": "1989-10-23", "city": "New Delhi, India", "category": "Energy & Power", "sector": "Power"},

    # 🏗️ 5. Infrastructure, Ports & Conglomerates
    "ADANIPORTS": {"name": "Adani Ports & SEZ Ltd", "date": "1998-05-26", "city": "Ahmedabad, India", "category": "Infrastructure", "sector": "Ports & Logistics"},
    "TATAMOTORS": {"name": "Tata Motors Ltd", "date": "1945-09-27", "city": "Mumbai, India", "category": "Automobile", "sector": "Auto"},
    "BHARTIARTL": {"name": "Bharti Airtel Ltd", "date": "1995-07-07", "city": "New Delhi, India", "category": "Telecom", "sector": "Telecom"},
    "ITC": {"name": "ITC Limited", "date": "1910-08-24", "city": "Kolkata, India", "category": "FMCG", "sector": "FMCG"},
    "LT": {"name": "Larsen & Toubro Ltd", "date": "1946-02-07", "city": "Mumbai, India", "category": "Infrastructure", "sector": "Engineering & Construction"}
}

SECTOR_ASTRO_MAP = {
    "All": {"ruling": "General Macro Baseline", "malefic_factor": 1.0},
    "Benchmark": {"ruling": "Sun / Jupiter / Saturn Axis", "malefic_factor": 1.05},
    "Banking": {"ruling": "Jupiter / Moon / Venus", "malefic_factor": 1.15},
    "Technology": {"ruling": "Mercury / Rahu / Uranus", "malefic_factor": 1.25},
    "Energy": {"ruling": "Mars / Saturn / Sun", "malefic_factor": 1.30},
    "Power": {"ruling": "Sun / Saturn / Mars", "malefic_factor": 1.20},
    "Metals": {"ruling": "Sun / Moon / Venus", "malefic_factor": 1.10}
}

class CorporateRiskEngine:
    def __init__(self):
        self.ep = EphemerisProvider()
        self.ep.set_sidereal_mode()

    def get_natal_positions(self, incorporation_date: datetime):
        """Calculates natal positions for a company/index (sidereal)."""
        jd = swe.julday(incorporation_date.year, incorporation_date.month, incorporation_date.day, 3.5)
        positions = {}
        for p_name, pid in self.ep.planet_ids.items():
            if p_name == 'Chiron': continue
            try:
                res, _ = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_SPEED)
                positions[p_name] = res[0]
            except:
                positions[p_name] = None
        return positions

    def analyze_company_horoscope(self, company_symbol: str, incorporation_date_str: str = None, current_smi: float = 5.5):
        """
        Dual Alignment Risk Analysis for NSE Stocks & Indices:
        Combines Mundane SMI Weather with Company/Index Personal Natal Transits & Dasha.
        """
        preset = PRESET_COMPANIES.get(company_symbol, {})
        
        if not incorporation_date_str:
            incorporation_date_str = preset.get("date", "1994-08-30")

        try:
            inc_date = datetime.strptime(incorporation_date_str, "%Y-%m-%d")
        except:
            inc_date = datetime.now()

        today = datetime.now()
        transit = self.get_natal_positions(today)
        natal = self.get_natal_positions(inc_date)

        company_name = preset.get("name", company_symbol)
        category = preset.get("category", "Equity Ticker")
        sector = preset.get("sector", "General")

        # --- Company Specific Personal Risk Score (Micro) ---
        micro_score = 5.0 # baseline 0 to 10
        signals = []

        t_saturn = transit.get('Saturn', 0)
        t_jupiter = transit.get('Jupiter', 0)
        t_rahu = transit.get('True_Node', 0)
        t_ketu = (t_rahu + 180) % 360 if t_rahu else 0

        n_sun = natal.get('Sun')
        n_moon = natal.get('Moon')
        n_saturn = natal.get('Saturn')
        n_jupiter = natal.get('Jupiter')
        n_mercury = natal.get('Mercury')

        # 1. Sade Sati / Kantaka Shani check (Saturn on Moon)
        if n_moon:
            diff = abs(t_saturn - n_moon)
            if diff > 180: diff = 360 - diff
            if diff < 12:
                micro_score += 2.8
                signals.append(f"{company_symbol}: Saturn Transit on Natal Moon (Sade Sati Peak - Organizational Stress)")

        # 2. Ketu on Natal Sun (Leadership / Identity crisis)
        if n_sun:
            diff = abs(t_ketu - n_sun)
            if diff > 180: diff = 360 - diff
            if diff < 10:
                micro_score += 2.2
                signals.append(f"{company_symbol}: Ketu Eclipsing Natal Sun (Governance & Regulatory Friction)")

        # 3. Rahu / Jupiter Beneficial Aspect
        if n_jupiter and t_jupiter:
            diff = abs(t_jupiter - n_jupiter)
            if diff > 180: diff = 360 - diff
            if diff < 15:
                micro_score -= 2.0
                signals.append(f"{company_symbol}: Jupiter Return Alignment (Expansion & Structural Growth Window)")

        if n_mercury and t_rahu:
            diff = abs(t_rahu - n_mercury)
            if diff > 180: diff = 360 - diff
            if abs(diff - 120) < 10:
                micro_score -= 1.8
                signals.append(f"{company_symbol}: Rahu Trine Mercury (Massive Digital Adoption & Innovation Drive)")

        micro_score = max(1.0, min(10.0, micro_score))

        # --- Dual Alignment Calculation ---
        dual_risk_index = round((current_smi * 0.5) + (micro_score * 0.5), 2)

        if dual_risk_index >= 7.5:
            recipe_status = "CRITICAL DISASTER RECIPE"
            recipe_desc = f"High Mundane SMI Weather + Malefic {company_symbol} Natal Transits. Extreme vulnerability to sharp price pullbacks."
        elif dual_risk_index >= 5.5:
            recipe_status = "MODERATE ELEVATED RISK"
            recipe_desc = f"Neutral to mixed alignment for {company_symbol}. Monitor sector trends and quarterly earnings."
        else:
            recipe_status = "GOLDEN EXPANSION WINDOW"
            recipe_desc = f"Benefic {company_symbol} Natal Dasha/Transits + Stable Mundane Baseline. Prime window for accumulation & breakout."

        return {
            "symbol": company_symbol,
            "company_name": company_name,
            "category": category,
            "incorporation_date": incorporation_date_str,
            "sector": sector,
            "mundane_smi_score": current_smi,
            "company_micro_risk": round(micro_score, 2),
            "dual_risk_index": dual_risk_index,
            "recipe_status": recipe_status,
            "recipe_desc": recipe_desc,
            "signals": signals if signals else [f"{company_symbol} natal chart operating within nominal baseline variance."]
        }
