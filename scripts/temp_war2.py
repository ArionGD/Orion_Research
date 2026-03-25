import pandas as pd
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.countries.manager import CountryManager

def angle_diff(lon1, lon2):
    diff = abs(lon1 - lon2) % 360
    return min(diff, 360 - diff)

def run_war_prophecy():
    provider = EphemerisProvider()
    cm = CountryManager()
    
    # Extending 15-day scans to the year 2055
    dates = pd.date_range(start='2026-01-01', end='2055-12-31', freq='15D')
    
    global_threats = []
    us_threats = []
    in_threats = []
    
    for dt in dates:
        pos = provider.get_all_positions(dt.to_pydatetime())
        t_pos = {}
        for k, v in pos.items(): t_pos[k.capitalize()] = v
        if 'Rahu' in t_pos: t_pos['True_node'] = t_pos['Rahu']
            
        ma_sa = angle_diff(t_pos.get('Mars', 0), t_pos.get('Saturn', 0))
        ma_ra = angle_diff(t_pos.get('Mars', 0), t_pos.get('True_node', 0))
        sa_ur = angle_diff(t_pos.get('Saturn', 0), t_pos.get('Uranus', 0))
        
        sys_war_score = 0
        if ma_sa < 5 or abs(ma_sa - 90) < 5 or abs(ma_sa - 180) < 5: sys_war_score += 10
        if ma_ra < 5 or abs(ma_ra - 90) < 5 or abs(ma_ra - 180) < 5: sys_war_score += 8
        if sa_ur < 5 or abs(sa_ur - 90) < 5 or abs(sa_ur - 180) < 5: sys_war_score += 12
        
        if sys_war_score > 0:
            global_threats.append({'Date': dt, 'Score': sys_war_score})
            
        us_s, us_sig = cm.check_risk('USA', t_pos)
        if us_s > 0:
             us_threats.append({'Date': dt, 'Score': us_s, 'Signals': us_sig})
             
        in_s, in_sig = cm.check_risk('India', t_pos)
        if in_s > 0:
             in_threats.append({'Date': dt, 'Score': in_s, 'Signals': in_sig})
        
    global_threats.sort(key=lambda x: x['Score'], reverse=True)
    print('\n=======================================')
    print('GLOBAL HOT WAR PROBABILITY (2026-2055)')
    print('=======================================')
    seen_w = set()
    for w in global_threats:
        y = w['Date'].year
        if y not in seen_w and len(seen_w) < 5: # Top 5 peak years
            seen_w.add(y)
            print(f'=> {w["Date"].strftime("%B %Y")} [Stress Score: {w["Score"]}/30]')
            
    us_threats.sort(key=lambda x: x['Score'], reverse=True)
    print('\n=======================================')
    print('USA: EXISTENTIAL/CIVIL CONFLICT PEAKS')
    print('=======================================')
    seen_us = set()
    for u in us_threats:
        y = u['Date'].year
        if y not in seen_us and len(seen_us) < 5:
            seen_us.add(y)
            print(f'=> {u["Date"].strftime("%B %Y")} (Threat Level: {u["Score"]:.1f})')
            for s in u['Signals']: print(f'     {s}')
            
    in_threats.sort(key=lambda x: x['Score'], reverse=True)
    print('\n=======================================')
    print('INDIA: SOVEREIGNTY / EXISTENTIAL PEAKS')
    print('=======================================')
    seen_in = set()
    track_in_years = []
    for i in in_threats:
        y = i['Date'].year
        if y not in seen_in:
            seen_in.add(y)
            track_in_years.append({'Year': y, 'Score': i['Score'], 'Date': i['Date'], 'Signals': i['Signals']})
    
    # Sort the India years chronologically to find the stabilization phase
    track_in_years.sort(key=lambda x: x['Year'])
    for ty in track_in_years:
        if ty['Score'] >= 25:
             print(f'=> {ty["Date"].strftime("%Y (%B)")} : CRITICAL MASS (Score {ty["Score"]:.1f})')
             for s in ty['Signals']: print(f'     {s}')
        elif ty['Score'] <= 5:
             pass # Skip minor noise
             
    print('\nSTABILIZATION ZERO-LINE YEARS (No major signals for India):')
    all_years = set(range(2026, 2056))
    stable_years = sorted(list(all_years - seen_in))
    print(stable_years)

if __name__ == '__main__':
    run_war_prophecy()
