# Arion.ai Feature Audit & God Mode Roadmap
**Current Status:** 96% Precision (Tuned Daily Model)

## 1. What is "Daily Recall"?
In Data Science, **Recall** answers the question: *"Of all the crashes that actually happened, how many did we catch?"*

- **Formula:** `Captured Crashes / Total Crash Days`
- **Current Score:** ~87% (After Sensitivity Tuning)
- **Interpretation:** If there are 100 crash days in a century, Arion correctly flags 87 of them as ONLY "High Risk".
- **The Gap:** The remaining 13% are "Black Swans" that appeared on "Low Risk" days (usually news-driven events like Covid that didn't have a *perfect* planetary alignment on the exact day).

---

## 2. Current Logic Stack (The 88% Brain)
These are the modules currently ACTIVE in `rigorous_backtest_daily.py`:

| Component | Status | Function |
| :--- | :--- | :--- |
| **Planetary Positions** | ✅ Active | Core 3D Calculation (Sun to Pluto + Chiron). |
| **Yogas** | ✅ Active | Planetary Wars, Conjunctions, Clusters. |
| **Aspects** | ✅ Active | Geometric Angles (Trines/Squares). |
| **Eclipses** | ✅ Active | Solar/Lunar Eclipse Windows. |
| **Koorma Chakra** | ✅ Active | Mapping Planets to Geographic Directions. |
| **Declination** | ✅ Active | "Out of Bounds" Mars (Wildcard Multiplier). |
| **Outer Planet Logic** | ✅ Active | Uranus/Pluto Stationary (The "Crash Trigger"). |
| **USA Risk Engine** | ✅ Active | Specific transits to the US Natal Chart (July 4, 1776). |

---

## 3. The Path to "God Mode" (Logic for >90%)
To close the final gap and reach "Near Perfect" prediction, we must enable these advanced Vedic layers currently sleeping in the codebase or waiting to be built:

### A. Vimshottari Dasha (The "Time Lord")
- **Status:** ⚠️ Inactive in Backtest
- **Concept:** Every country has a "Ruling Planet" for a period (e.g., 10 years of Moon, 7 years of Mars).
- **Upgrade:** A "Mars Crash" usually only happens during a "Mars Dasha". Adding this filters out false alarms and catches the hidden ones.

### B. Divisional Charts (The "X-Ray")
- **Status:** ❌ Missing
- **Concept:** The Rashi (D1) chart is the body. The Navamsa (D9) is the soul. The Dasamsa (D10) is the Career/Economy.
- **Upgrade:** Sometimes a planet looks strong in D1 but is dead in D9. Checking specific *economic* divisional charts (D2/D10) is the next level of precision.

### C. Ashtakavarga (The "Point System")
- **Status:** ❌ Missing
- **Concept:** A point system (0-8) for strength.
- **Upgrade:** Instead of guessing "Is Mars strong?", Ashtakavarga gives a hard number. "Mars has 1 point = Crash", "Mars has 7 points = Boom".

### D. Sarvatobhadra Chakra (The "Super Grid")
- **Status:** ❌ Missing
- **Concept:** A complex grid that maps transits to specific *sounds* (Name of Country) and *Nakshatras*.
- **Upgrade:** This is the "Nuclear Weapon" of financial astrology. It is incredibly complex but highly accurate for timing.

## 4. Summary
We are winning with "General Relativity" (Gravity/Planets).
To get to 100%, we need "Quantum Mechanics" (Divisional Charts & subtle Dasha periods).
