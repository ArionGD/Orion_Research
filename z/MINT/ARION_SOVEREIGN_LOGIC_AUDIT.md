# 🛡️ Arion Sovereign Logic Audit (v4.5)
**Document Purpose:** A complete institutional record of all astronomical, technical, and mathematical factors currently being computed by the Arion AI Ensemble.

---

## 🌌 1. The Astronomical Core (Celestial Logic)
These features drive the "Sentiment" and "Systemic Gravity" layers of the brain.

### **A. Geocentric (Earth-View) — "Human Sentiment/Panic"**
We compute the **Longitude (0-360°)**, **Speed**, and **Retrograde State** for:
*   **Lights:** Sun, Moon.
*   **Inner Planets:** Mercury, Venus, Mars.
*   **Outer Planets:** Jupiter, Saturn, Uranus, Neptune, Pluto.
*   **Lunar Nodes:** True Node, Ketu (180° opposite).

### **B. Heliocentric (Sun-View) — "True Systemic Velocity"**
Used to bypass the "Optical Illusion" of retrogrades and see pure orbital physics.
*   **Planets Calculated:** Mars_Helio, Jupiter_Helio, Saturn_Helio, Uranus_Helio.
*   **Metric:** Longitude and Speed (Orbital Velocity).

### **C. Declination Physics (Z-Axis Momentum)**
*   **Weighted OOB (Out-of-Bounds):** Tracks when the Moon or Mars goes beyond 23.44° declination.
*   **Feature:** `Mars_OOB_Intensity` and `Moon_OOB_Intensity`.

---

## 📐 2. The Medini Logic Modules (Elite Scaling)

### **A. Gann "Square of 9" Price-to-Lon Upgrade**
*   **Transformation:** We translate the Index Price (5000+) into a Zodiac Degree.
*   **Wrapping:** We use a Log-Magnitude scale factor (10, 100, 1000) to ensure the price degree wraps correctly around the 360° circle.
*   **Collision Detection:** We flag whenever the **Price Longitude** hits a "Hard Aspect" (0°, 90°, 180°, 270°) with **Saturn** or **Mars**.

### **B. Bradley Siderograph Oscillator (1948)**
*   **The Engine:** A weighted aspect line of "Market Energy."
*   **Planetary Weights:**
    *   Jupiter (+5.0), Venus (+4.0), Mars (+3.0)
    *   Saturn (-5.0), Uranus (-4.0), Neptune (-3.0)
*   **Weights for Aspects:** Conjunction (+10), Trine (+8), Square (-5), Opposition (-8).
*   **Output:** A single numerical `Bradley_Score` fed directly into the ML layers.

### **C. Havoc Cycles (Global Risk)**
*   **Saturn-Neptune (Havoc):** 36-year cycle. We calculate the exact angular distance and its velocity.
*   **Planetary Wars (Yogas):** Detects when Mars and Saturn are within 1° (Global Failure Trigger).

---

## 📈 3. The Structural Financial Floor (Money Logic)

### **A. Volatility & Liquidity Plumbing**
*   **VIX Backwardation Ratio:** Spot VIX vs. 20-week SMA (Higher than 1.30 = Structural Failure).
*   **Synthetic GEX Proxy:** Calculates Dealer Gamma pressure by correlating Price Momentum vs. Volatility Slope.
*   **VIX Stress Ratio:** Current VIX vs. 50-week "Long-term Normal."

### **B. The "Recession" Logic (Yield Curves)**
*   **Inversion Signal:** Spread between 10-Year and 3-Month Treasury Yields.
*   **Metric:** `Yield_Curve_Inverted` (1 if negative).

### **C. Price Momentum (Trend Integrity)**
*   **Momentum:** 4-week and 12-week price rate of change.
*   **Volatility:** 20-week Rolling Standard Deviation of Log Returns.

---

## 🎯 4. Target Definitions (The "Kill List")
Arion is currently training to catch 3 specific events:
1.  **Macro (Big Gun):** Positive Return in the next **6 Months** (Safety Signal).
2.  **Sniper (Precision):** Lower price (-3% or more) in the next **3 Months** (Short/Crash Signal).
3.  **Assault (Intraday):** Lower price (-2% or more) in the next **4 Weeks** (Flash Drop Signal).

---

## 🚀 5. Resolution & Training Specs
*   **Resolution:** Weekly (Monday Open to Friday Close).
*   **Training Samples:** 5,125 weeks (100 Years of Mastery).
*   **The Sovereign Guard:** Logic thresholds set between 80% and 90% confidence to stop false alarms.
