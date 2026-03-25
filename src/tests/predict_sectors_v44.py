"""
Arion.ai Sector Predictor v4.4
=================================
Enhanced sector prediction engine with:
1. Conflict Modifier (hot war vs cold siege detection)
2. Havoc Integration (cross-sector contagion during global crises)
3. Complete Aspect Coverage (trines, squares, oppositions, Vedic aspects)
4. AI Disruption Factor (legacy IT vs new-age tech split)

Fixes applied from March 2026 post-mortem analysis.
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.yogas import YogaScanner
from src.engine.medini.conflict_modifier import ConflictModifier
from src.engine.world.havoc_logic import GlobalHavocLogic
import swisseph as swe


def get_sector_map():
    return {
        'Tech & AI (New Age)': ['Mercury', 'True_Node'],     # Mercury (Logic) + Rahu (Innovation)
        'Tech & AI (Legacy IT)': ['Mercury', 'Saturn'],       # Mercury (IT) + Saturn (Old/Established)
        'Banking & Finance': ['Jupiter', 'Venus'],            # Jupiter (Wealth) + Venus (Cash)
        'Energy & Metals': ['Saturn', 'Mars'],                # Saturn (Oil/Coal) + Mars (Energy/Metal)
        'Real Estate': ['Mars', 'Saturn'],                    # Mars (Land) + Saturn (Construction)
        'Pharma & Health': ['Sun', 'Ketu'],                   # Sun (Vitality) + Ketu (Viruses/Chems)
        'Auto & Transport': ['Venus', 'Mercury'],             # Venus (Vehicles) + Mercury (Logistics)
    }


def analyze_sector_perf(planet_positions, ep, date, prev_date=None):
    """
    Enhanced sector performance analysis.
    Now includes: conflict modifiers, havoc contagion, and complete aspect coverage.
    """
    scores = {k: 0 for k in get_sector_map().keys()}
    signals = {k: [] for k in get_sector_map().keys()}

    # =============================================
    # LAYER 1: PLANET DIGNITY (Exaltation/Debilitation)
    # =============================================
    for sector, planets in get_sector_map().items():
        score = 0

        for p in planets:
            if p not in planet_positions:
                continue
            lon = planet_positions[p]

            # --- Exaltations ---
            if p == 'Mars' and 270 <= lon <= 300:
                score += 5
                signals[sector].append(f"{p} Exalted (Capricorn)")

            if p == 'Venus' and 330 <= lon <= 360:
                score += 5
                signals[sector].append(f"{p} Exalted (Pisces)")

            if p == 'Jupiter' and 90 <= lon <= 120:
                score += 5
                signals[sector].append(f"{p} Exalted (Cancer)")

            if p == 'Mercury' and 150 <= lon <= 180:
                score += 4
                signals[sector].append(f"{p} Exalted (Virgo)")

            if p == 'Sun' and 0 <= lon <= 30:
                score += 4
                signals[sector].append(f"{p} Exalted (Aries)")

            # --- Debilitations ---
            if p == 'Mars' and 90 <= lon <= 120:
                score -= 5
                signals[sector].append(f"{p} Debilitated (Cancer)")

            if p == 'Saturn' and 0 <= lon <= 30:
                score -= 5
                signals[sector].append(f"{p} Debilitated (Aries)")

            if p == 'Mercury' and 330 <= lon <= 360:
                score -= 4
                signals[sector].append(f"{p} Debilitated (Pisces)")

            if p == 'Venus' and 150 <= lon <= 180:
                score -= 4
                signals[sector].append(f"{p} Debilitated (Virgo)")

            # =============================================
            # LAYER 2: COMPLETE ASPECT COVERAGE
            # =============================================

            # --- Jupiter Aspects (Benefic) ---
            jup_lon = planet_positions.get('Jupiter')
            if jup_lon:
                diff = abs(lon - jup_lon)
                if diff > 180:
                    diff = 360 - diff

                # Trine (120°) — Strong positive
                if abs(diff - 120) < 10:
                    score += 3
                    signals[sector].append(f"Jupiter Trine {p}")

                # Conjunction (0°) — Positive expansion
                if diff < 10:
                    score += 2
                    signals[sector].append(f"Jupiter Conjunct {p}")

                # Sextile (60°) — Mild positive
                if abs(diff - 60) < 8:
                    score += 1
                    signals[sector].append(f"Jupiter Sextile {p}")

                # Opposition (180°) — Tension but can be growth
                if abs(diff - 180) < 10:
                    score -= 1
                    signals[sector].append(f"Jupiter Opposition {p}")

            # --- Saturn Aspects (Malefic) ---
            sat_lon = planet_positions.get('Saturn')
            if sat_lon:
                diff = abs(lon - sat_lon)
                if diff > 180:
                    diff = 360 - diff

                # Conjunction (0°) — Restriction/Compression
                if diff < 10:
                    score -= 4
                    signals[sector].append(f"Saturn Conjunct {p}")

                # Opposition (180°) — Direct conflict/obstruction
                if abs(diff - 180) < 10:
                    score -= 3
                    signals[sector].append(f"Saturn Opposition {p}")

                # Square (90°) — Friction and obstacles
                if abs(diff - 90) < 8:
                    score -= 3
                    signals[sector].append(f"Saturn Square {p}")

                # Vedic 3rd aspect (60°) — Mild restriction
                if abs(diff - 60) < 6:
                    score -= 1
                    signals[sector].append(f"Saturn 3rd Aspect {p}")

                # Vedic 10th aspect (270° / effectively 90° in reverse context)
                # Already covered by square check above

            # --- Mars Aspects (Aggressive volatility) ---
            mars_lon = planet_positions.get('Mars')
            if mars_lon and p != 'Mars':
                diff = abs(lon - mars_lon)
                if diff > 180:
                    diff = 360 - diff

                # Conjunction — Intense energy (can be positive for Energy sector)
                if diff < 8:
                    if sector in ['Energy & Metals']:
                        score += 2  # Mars conjunction boosts energy
                    else:
                        score -= 2  # But destabilizes other sectors
                    signals[sector].append(f"Mars Conjunct {p}")

                # Square (90°) — Aggressive friction
                if abs(diff - 90) < 8:
                    score -= 2
                    signals[sector].append(f"Mars Square {p}")

                # Vedic 4th aspect (90°) already covered
                # Vedic 8th aspect (210°)
                if abs(diff - 210) < 6:
                    score -= 2
                    signals[sector].append(f"Mars 8th Aspect {p}")

            # --- Rahu (True_Node) Influence ---
            rahu_lon = planet_positions.get('True_Node')
            if rahu_lon and p != 'True_Node':
                diff = abs(lon - rahu_lon)
                if diff > 180:
                    diff = 360 - diff

                # Rahu conjunction — Disruption / Innovation (context dependent)
                if diff < 10:
                    if 'New Age' in sector:
                        score += 3  # Rahu boosts innovation/new-age
                        signals[sector].append(f"Rahu Conjunct {p} (Innovation Boost)")
                    elif 'Legacy' in sector:
                        score -= 3  # Rahu disrupts legacy/established
                        signals[sector].append(f"Rahu Conjunct {p} (Disruption Risk)")
                    else:
                        score -= 1  # General instability
                        signals[sector].append(f"Rahu Conjunct {p}")

                # Rahu trine — Amplified growth for new-age
                if abs(diff - 120) < 10:
                    if 'New Age' in sector:
                        score += 2
                        signals[sector].append(f"Rahu Trine {p} (Tech Innovation)")
                    elif 'Legacy' in sector:
                        score -= 2  # Legacy gets disrupted even from trine
                        signals[sector].append(f"Rahu Trine {p} (AI Disruption Pressure)")

        scores[sector] = score

    # =============================================
    # LAYER 3: CONFLICT MODIFIER (War Detection)
    # =============================================
    conflict_mod = ConflictModifier()
    conflict_analysis = conflict_mod.analyze_conflict(planet_positions, date)

    if conflict_analysis['conflict_active']:
        for sector, modifier in conflict_analysis['sector_modifiers'].items():
            if sector in scores:
                scores[sector] += modifier
                if modifier != 0:
                    war_type = conflict_analysis['conflict_type'].replace('_', ' ').title()
                    direction = "↑" if modifier > 0 else "↓"
                    signals[sector].append(
                        f"War Modifier ({war_type}): {direction}{abs(modifier)}"
                    )

    # =============================================
    # LAYER 4: HAVOC CONTAGION (Global Crisis Penalty)
    # =============================================
    havoc = GlobalHavocLogic()
    havoc_features = havoc.calculate_havoc_features(date, prev_date)

    if havoc_features:
        gsi = havoc_features.get('Global_Stability_Index', 900)
        velocity = abs(havoc_features.get('Havoc_Velocity', 0))
        oob_count = havoc_features.get('OOB_Count', 0)

        # Normalize: GSI typically 600-1200. Below 750 = stress.
        # Havoc velocity > 30 = significant shock.
        crisis_level = 0

        if gsi < 750:
            crisis_level += 1
            if gsi < 600:
                crisis_level += 1

        if velocity > 30:
            crisis_level += 1
            if velocity > 60:
                crisis_level += 1

        if oob_count >= 2:
            crisis_level += 1

        # Apply contagion penalty if crisis detected
        if crisis_level >= 2:
            contagion_penalty = crisis_level * -2
            for sector in scores:
                # Energy gets LESS penalty during hot war (already handled by conflict modifier)
                if sector == 'Energy & Metals' and conflict_analysis.get('conflict_type') == 'hot_war':
                    scores[sector] += max(contagion_penalty + 3, 0)  # Reduced penalty
                elif 'Pharma' in sector:
                    scores[sector] += max(contagion_penalty + 2, 0)  # Defensive sector
                else:
                    scores[sector] += contagion_penalty

                signals[sector].append(f"Havoc Contagion (Level {crisis_level}): {contagion_penalty:+d}")

    # =============================================
    # LAYER 5: AI DISRUPTION MODIFIER
    # =============================================
    # Ketu in Virgo (150-180°) = deep code optimization → bearish for legacy IT outsourcing
    ketu_lon = planet_positions.get('Ketu')
    if ketu_lon and 150 <= ketu_lon <= 180:  # Ketu in Virgo
        if 'Tech & AI (Legacy IT)' in scores:
            scores['Tech & AI (Legacy IT)'] -= 3
            signals['Tech & AI (Legacy IT)'].append("Ketu in Virgo: AI cannibalizing legacy outsourcing")
        if 'Tech & AI (New Age)' in scores:
            scores['Tech & AI (New Age)'] += 2
            signals['Tech & AI (New Age)'].append("Ketu in Virgo: Favors AI-native companies")

    return scores, signals


def predict_next_3_months():
    print("=== Arion.ai 90-Day Prophet v4.4 (Enhanced Sector Scan) ===")

    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)

    start_date = datetime.now()
    end_date = start_date + timedelta(days=90)

    print(f"Scanning from {start_date.date()} to {end_date.date()}...\n")

    results = []

    current = start_date
    prev = None
    while current <= end_date:
        pos = ep.get_all_positions(current)
        sector_scores, sector_sigs = analyze_sector_perf(pos, ep, current, prev)

        row = {'Date': current}
        row.update(sector_scores)

        # Store signals for peak days
        row['Signals'] = sector_sigs

        results.append(row)
        prev = current
        current += timedelta(days=1)

    df = pd.DataFrame(results)

    # Generate Report
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'x', 'forecast_v44_sectors.md')
    output_path = os.path.normpath(output_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Arion.ai 3-Month Alpha Report v4.4 ({start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')})\n")
        f.write("**Medini Engine v4.4 — Enhanced with Conflict Modifier, Havoc Contagion, Complete Aspects**\n\n")

        f.write("## 🚀 Sector Recommendations (Overview)\n\n")

        # Calculate Aggregates
        sector_cols = [c for c in df.columns if c not in ['Date', 'Signals']]
        avg_scores = df[sector_cols].mean()
        top_sector = avg_scores.idxmax()
        worst_sector = avg_scores.idxmin()

        f.write(f"### 🏆 Top Investment: **{top_sector}** (Score: {avg_scores[top_sector]:.1f})\n")
        f.write(f"### ⚠️ Short Candidate: **{worst_sector}** (Score: {avg_scores[worst_sector]:.1f})\n\n")

        f.write("---\n\n")

        # ---- Conflict Status ----
        f.write("## ⚔️ Conflict Analysis\n")
        latest_pos = ep.get_all_positions(start_date)
        conflict_mod = ConflictModifier()
        conflict_result = conflict_mod.analyze_conflict(latest_pos, start_date)
        f.write(conflict_mod.get_summary(conflict_result))
        f.write("\n\n---\n\n")

        # ---- Month-by-Month ----
        f.write("## 📅 Month-by-Month Breakdown\n")

        # Group by Month
        df['Month'] = df['Date'].dt.strftime('%B %Y')
        for month, group in df.groupby('Month', sort=False):
            f.write(f"### {month}\n")

            # Find best/worst days in this month
            m_avg = group[sector_cols].mean()
            best_sec_m = m_avg.idxmax()
            curr_score = m_avg[best_sec_m]

            f.write(f"- **Focus Sector:** {best_sec_m} (Avg Score: {curr_score:.1f})\n")

            # Check specific signals from first few days to see context
            sample_sigs = group.iloc[0]['Signals'].get(best_sec_m, [])
            if sample_sigs:
                f.write(f"- **Key Driver:** {', '.join(list(set(sample_sigs))[:3])}\n")

            f.write("| Sector | Outlook | Score | Logic |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")

            for sec in get_sector_map().keys():
                s = m_avg[sec]
                if s > 4:
                    outlook = "🟢 STRONG BUY"
                elif s > 2:
                    outlook = "🟢 BUY"
                elif s > -2:
                    outlook = "🟡 HOLD"
                elif s > -4:
                    outlook = "🔴 SHORT"
                else:
                    outlook = "🔴 STRONG SHORT"

                # Get signals
                uniq_sigs = []
                for _, r in group.iterrows():
                    sigs = r['Signals'].get(sec, [])
                    if sigs:
                        uniq_sigs.extend(sigs)

                logic_str = ", ".join(list(set(uniq_sigs))[:4])  # First 4 unique
                f.write(f"| {sec} | {outlook} | {s:.1f} | {logic_str} |\n")

            f.write("\n")

    print(f"Enhanced Forecast Report Generated: {output_path}")
    return df


if __name__ == "__main__":
    predict_next_3_months()
