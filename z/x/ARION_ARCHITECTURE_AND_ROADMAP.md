# Arion.ai Technical Documentation & Roadmap

## 1. System Architecture (The 'Super AI' Structure)

Arion.ai is architected as a **Modular, Hybrid Predictive Engine**, not a monolithic script. It mimics a distributed "Global Brain" where specialized agents utilize a universal mathematical core to feed a central synthesis layer.

### Core Layers
*   **Universal Math Layer:** `src/engine/core/ephemeris_provider.py`
    *   The single source of truth for planetary positions, ensuring 100% consistency across all modules.

*   **Global Brain:** `src/engine/world/havoc_logic.py`
    *   Calculates the **Barbault Global Stability Index (GSI)**.
    *   Monitors "Planetary Compression" (when all planets gather within a narrow arc), a key historical correlate for world events.

### Specialist Modules
Independent logic centers that track specific risk vectors:
*   **`saturn_neptune/`**: Tracks the "Master Cycle" of long-term economic trends and structural dissolution.
*   **`mars/`**: The "Kinetic Trigger." Calculates Volatility Scores based on speed, retrograde motion, and World Point axis hits.
*   **`speculation_logic.py`**: Monitors Venus-Uranus interactions to detect "Flash Crash" or sudden liquidity events.
*   **`planets/`**: (New) Dedicated logic silos for every celestial body (Sun through Ketu) to handle granular specificities.

### The Sentinel
*   **`src/alerts/`**: A watchdog module that specifically monitors the **NYSE Natal Chart**. It checks for direct planetary hits (Transits to Natal) that affect the exchange's vitality.

### The Translator
*   **`src/world/translator.py`**: The synthesis engine. It aggregates raw scores from Havoc, Mars, and Specialist modules to generate human-readable "C-Suite Executive Summaries" and Tiered Risk Reports.

---

## 2. The Current Prophecy (2026-2027 Outlook)

The model is currently tracking a sequence of high-probability stress events based on the 100-year backtested correlation:

*   **Feb 2026: 🚨 CRITICAL (100% Risk)**
    *   **trigger:** Uranus Station + Venus Square + Direct hit on NYSE Sun.
    *   **Prediction:** A major Liquidity Event or sudden market dislocation.

*   **July 2026: 📉 Structural Stress**
    *   **Trigger:** The **Global Stability Index (GSI)** reaches massive compression as the Saturn-Neptune conjunction tightens.
    *   **Prediction:** A period of "Deep Freeze" or structural reorganization (Recessionary pressure).

*   **Jan 2027: 💥 Kinetic Trigger**
    *   **Trigger:** Mars makes a hard aspect (Square/Opposition) to the **0° Aries World Point** while the outer planets are compressed.
    *   **Prediction:** A volatile breakout or geopolitical shock.

---

## 3. Model Evolution (The 'Brain' History)

*   **V1: Random Forest (62% Accuracy)**
    *   Initial ML approach using raw planetary longitudes. Failed to capture the nuance of "Special Yogas."

*   **V2: Hybrid Rule-Based Model (Current)**
    *   Integrates Vedic Yogas, Western Aspects, and GSI.
    *   **Key Findings (Feature Importance):**
        1.  **Saturn-Neptune Angle:** The dominant cycle for global trends.
        2.  **Global Stability Index (GSI):** The best predictor of general macro stress.
        3.  **Mars Volatility:** The most reliable timer for *when* a crash happens.

*   **V3 (Next Generation): XGBoost + LSTM**
    *   Planning to implement Self-Correcting Neural Networks to detect non-linear patterns between sentiment data and planetary geometry.

---

## 4. Future Roadmap (The '3D' Upgrade)

**Objective:** Evolve from "2D Map" logic (Longitude only) to "3D Holographic" reality (High-Fidelity Astro-Physics).

### Upgrade A: Declination (The Z-Axis)
*   **Concept:** Planets aren't just on a circle; they move up and down.
*   **Goal:** Detect **"Out of Bounds"** planets (Declination > 23.5°). Historically, Mars or Moon OOB correlates with extreme, irrational volatility.

### Upgrade B: Lunar Nodes (The Destiny Axis)
*   **Concept:** Rahu (North Node) and Ketu (South Node) are the intersection points of the Moon and Sun's paths.
*   **Goal:** Identify **"Destiny Triggers"** (Eclipses) with granular precision. Explicitly model the "Vipat" (Danger) Nakshatras.

### Upgrade C: The Volatility Backtester
*   **Concept:** Price is noisy; Fear is signal.
*   **Goal:** Correlate 'Havoc Scores' directly with the **VIX (Volatility Index)** from 1990-2025 to tune the sensitivity of the Mars Module.

### Upgrade D: Automated Sentinel
*   **Concept:** Passive monitoring.
*   **Goal:** CRON Jobs running daily digests, pushing mobile alerts only when the Risk Tier shifts from "SAFE" to "WARNING" or "CRITICAL".
