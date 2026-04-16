import pandas as pd
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.countries.manager import CountryManager

def angle_diff(lon1, lon2):
    diff = abs(lon1 - lon2) % 360
    return min(diff, 360 - diff)

def run_war_prophecy():
    provider = EphemerisProvider()
    cm = CountryManager()
    
    dates = pd.date_range(start='2029-01-01', end='2034-12-31', freq='15D')
    
    global_threats = []
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
             
        in_s, in_sig = cm.check_risk('India', t_pos)
        if in_s > 0:
             in_threats.append({'Date': dt, 'Score': in_s, 'Signals': in_sig})
        
    global_threats.sort(key=lambda x: x['Score'], reverse=True)
    print('*** WORLD TENSION ***')
    seen_w = set()
    for w in global_threats:
        y_m = w['Date'].strftime('%Y-%m')
        if y_m not in seen_w and len(seen_w) < 4:
            seen_w.add(y_m)
            print(f'=> {w["Date"].strftime("%B %Y")} [Global War Stress Score: {w["Score"]}/30]')
            
    in_threats.sort(key=lambda x: x['Score'], reverse=True)
    print('\n*** INDIA THREAT ***')
    seen_in = set()
    for i in in_threats:
        y = i['Date'].year
        if y not in seen_in and len(seen_in) < 6:
            seen_in.add(y)
            print(f'=> {i["Date"].strftime("%B %Y")} (Threat Level: {i["Score"]:.1f})')
            for s in i['Signals']: print(f'   - {s}')

if __name__ == '__main__':
    run_war_prophecy()
