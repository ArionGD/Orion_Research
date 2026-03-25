# Arion.ai: Medini Jyotish Expansion Roadmap

## Current State Analysis
**Existing Data:**
- **Planets:** Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, True Node (Rahu). (Western/Neo-Vedic mix)
- **Logic:** Barbault's Cyclical Index (Western Mundane), Declination, Retrograde, simple Aspects ($0^\circ, 90^\circ, 180^\circ$).
- **Missing vs. Medini Jyotish:**
    1.  **Ketu (South Node):** Essential karmic point, 180° from Rahu. Used for predicting "crashes" and "separations".
    2.  **Nakshatras (Lunar Mansions):** The core of Vedic positioning (27 stars). Currently only raw longitude is tracked.
    3.  **Rasi (Zodiac Signs):** Explicit Sign entry and Ingress (Sankranti) data.
    4.  **Graha Yudha (Planetary War):** Critical for conflict prediction.
    5.  **Eclipses:** Specific flags for Solar/Lunar eclipses.
    6.  **Panchang Elements:** Tithi, Yoga, Karana (optional for macro, but good for timing).

## Phase 1: The Foundation - Completing the Grahas & Zodiac
**Goal:** Ensure the engine perceives the "Full Sky" in Vedic terms.
- [x] **Step 1:** Add **Ketu (South Node)** calculation to `ephemeris_provider.py`.
- [x] **Step 2:** Implement **Sidereal Ayanamsa** support. (Current engine might be Tropical/Western; Medini requires Sidereal/Lahiri). *Critical Check needed.*
- [x] **Step 3:** Implement **Zodiac Sign (Rasi)** calculation (Aries, Taurus, etc.).
- [x] **Step 4:** Implement **Nakshatra** calculation (0-27 mapping) and Padas (1-4).

## Phase 2: The Conjunction Engine (Yoga Logic)
**Goal:** Detect interactions specific to Global Events.
- [x] **Step 1:** Build a `ConjunctionScanner` to find precise 0° alignments (Yogas).
- [x] **Step 2:** Implement specific Vedic Yogas for Finance:
    - *Guru-Chandal Yoga* (Jupiter + Rahu) -> Market Corruption/Expansion bubbles.
    - *Angarak Yoga* (Mars + Rahu) -> Violence/Volatile Crashes.
    - *Shani-Mangal* (Saturn + Mars) -> Conflict/Recession.
- [x] **Step 3:** Integrate Graha Yudha (Planetary War) detection.

## Phase 3: The Temporal Dimension (time & Eclipses)
**Goal:** Pinpoint "When" events happen.
- [x] **Step 1:** Eclipse Detector (Rahu/Ketu axis proximity to Sun/Moon).
- [x] **Step 2:** Ingress (Sankranti) detection (Sun changing signs).
- [x] **Step 3:** Retrogression Start/End precise timing.

## Phase 4: Financial & Sector Synthesis
**Goal:** "Where to Invest?"
- [x] **Step 1:** Map Planets to Industry Sectors (Medini standard).
    - *Mars*: Real Estate, Military, Crypto.
    - *Mercury*: Trade, Tech, Communication.
    - *Jupiter*: Banking, Finance, Law.
- [x] **Step 2:** Update `translator.py` to use new Yogas for Executive Reporting.
- [x] **Step 3:** Backtest specific Yogas against `century_master.csv` data.
