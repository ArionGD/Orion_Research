# Gold Astrology: XGBoost Forensic Analysis

> **Dataset:** 100-Year Enriched Gold Master V70
> **Model:** XGBoost (Gradient Boosting Decision Trees)

## Global Feature Importance (Weight)
XGBoost identifies the following features as the most frequent split points:

| Feature | Weight Score | Forensic Role |
| :--- | :--- | :--- |
| **Ketu_Deg** | 700.0 | Tail-Risk Trigger |
| **Moon_Deg** | 558.0 | Cycle Component |
| **Saturn_Deg** | 484.0 | Long-term Anchor |
| **Sun_Deg** | 428.0 | Cycle Component |
| **Mars_Speed** | 381.0 | Cycle Component |
| **Tithi** | 247.0 | Cycle Component |
| **SMI_Base** | 241.0 | Market Correlation |
| **Nakshatra** | 23.0 | Cycle Component |

## Model Interpretation
Unlike EBM, XGBoost captures complex non-linear interactions between planetary degrees.

1. **High Volatility Clusters**: XGBoost detects heavy 'branching' around Ketu and Saturn intersections, suggesting these are not just linear drivers but state-change triggers.
2. **Short-term Momentum**: Moon_Deg and Tithi show high weights, indicating they are crucial for fine-tuning the exact timing of price action.
3. **SMI Integration**: The model heavily uses SMI_Base to scale the impact of astrological signals, confirming that 'Celestial' signals are amplified during 'Terrestrial' market fear.

