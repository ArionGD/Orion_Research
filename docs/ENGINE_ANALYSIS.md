# ORION Sovereign Intelligence Engine: Technical Analysis

The **ORION (ARION CORE)** engine is a high-resolution market analysis system that merges **Advanced Medini Jyotish (Mundane Astrology)** with modern financial engineering (Gann Geometry, Bradley Oscillators, and Options Flow).

## Evolution of the Engine

| Feature | Old Version (Streamlit) | New Version (v5.5 FastAPI) |
| :--- | :--- | :--- |
| **Architecture** | Monolithic Python/Streamlit UI | Lean JSON API + Shadow Engines |
| **Primary Output** | Dashboard Visuals / Reports | SMI (Sovereign Malefic Index) Score |
| **Intraday** | Gann Wheel of 24 | Sniper Sniper/Execution Layer |
| **Integration** | Standalone Dashboard | PHOENIX Dashboard (Svelte/FastAPI) |

---

## Core Engine Components

### 1. Sovereign Malefic Index (SMI)
The SMI is the heartbeat of the engine, providing a risk score from **0 to 10.0**.
*   **Logic File**: `src/engine/medini/crash_logic.py`
*   **Key Drivers**:
    *   **Graha Yuddha (Planetary War)**: High risk when Mars and Saturn are within 1°.
    *   **Dasha Logic**: Timing factors based on whether the ruling lords (Mahadasha/Antardasha) are malefics.
    *   **Outer Aspects**: Hard aspects (0°, 90°, 180°) between Saturn and Neptune (the "Havoc Cycle").

### 2. Gann Price-to-Longitude Translator
Translates market prices (S&P 500/Nifty) into 360° zodiacal coordinates.
*   **Formula**: `Angle = ((SQRT(Price) * 180) - 225) % 360`
*   **Purpose**: Detects "collisions" where the price level hits a planetary degree, signaling an absolute top or bottom.

### 3. Bradley Siderograph Oscillator
A mathematical model assigning weights to planetary aspects to predict "Market Energy."
*   **Weights**:
    *   **Bullish (+)**: Trines (120°), Sextiles (60°).
    *   **Bearish (-)**: Squares (90°), Oppositions (180°).
*   **Implementation**: `src/engine/medini/bradley_oscillator.py`

### 4. Medini Synthesizer
The orchestration layer that scans for Vedic Yogas and Temporal events (Eclipses).
*   **Scanner**: `YogaScanner` searches for specific planetary pairs and triplets.
*   **Sector Mapping**: Translates planetary influences into market sectors (e.g., Saturn hit = Tech crash, Jupiter hit = BFSI rally).

---

## Key Forensic Windows
The engine is specifically tuned for structural resets:
*   **March 2020**: Caught at SMI 9.2 (COVID Reset).
*   **April 19, 2026**: Predicted **SMI 9.4 (CRITICAL)**.

---

## Shadow Engines (Project ARGOS)
The latest version (v5.5) has classified **ARGOS** as a "Shadow Engine" for institutional flow and dark pool analysis, which runs locally-only for privacy.

---

### **Recommendation for Development**
To reach the planned **ACE v5.5 Ultra Alpha**, the focus should be on:
1.  **VPIN + GEX Overlay**: Merging the Astro-timing with live Options Flow (Gamma Exposure).
2.  **Transformer-based Logic**: Replacing XGBoost with LSTMs to capture the "rhythm" of cycles.
3.  **Heliocentric Processing**: Using Sun-centered coordinates for "True Systemic Velocity."
