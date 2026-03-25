from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.planets.mars.general import MarsGeneralLogic
from src.engine.astro.core.declination import DeclinationLogic
from datetime import datetime, timedelta
import swisseph as swe

def run_audit():
    print("=== ARION.AI 2026 CRITICAL AUDIT (3D MODE) ===")
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI) # Vedic align
    
    mars_engine = MarsGeneralLogic()
    decl_logic = DeclinationLogic()
    
    start_date = datetime(2026, 2, 1)
    end_date = datetime(2026, 2, 15)
    
    curr = start_date
    while curr <= end_date:
        # Check Mars
        res_mars = mars_engine.calculate_volatility(curr)
        m_decl = res_mars.get('Mars_Decl', 0)
        m_oob = res_mars.get('Mars_OOB', False)
        
        # Check Venus OOB too
        _, _, _, v_decl = ep.get_planet_data(curr, 'Venus')
        v_oob = decl_logic.is_out_of_bounds(v_decl)
        
        # Check Node Proximity to Outer Planets
        nodes = ep.get_true_nodes(curr)
        rahu = nodes['Rahu']
        ketu = nodes['Ketu']
        
        outer_hits = []
        if rahu is not None:
             for op in ['Saturn', 'Uranus', 'Neptune', 'Pluto']:
                 op_lon, _, _, _ = ep.get_planet_data(curr, op)
                 if op_lon:
                     dist_r = ep.get_distance(op_lon, rahu)
                     dist_k = ep.get_distance(op_lon, ketu)
                     
                     if dist_r < 3.0 or dist_k < 3.0:
                         outer_hits.append(f"{op}-Node")
        
        
        # Output
        date_str = curr.strftime("%Y-%m-%d")
        
        status = "NORMAL"
        if m_oob or v_oob:
            status = "⚠️ OOB (High Volatility)"
        if outer_hits:
            status += f" | 💥 NODE TRIGGER: {outer_hits}"
            
        print(f"{date_str} | Mars Decl: {m_decl:.2f} (OOB: {m_oob}) | Venus Decl: {v_decl:.2f} (OOB: {v_oob}) | {status}")
        
        curr += timedelta(days=1)

if __name__ == "__main__":
    run_audit()
