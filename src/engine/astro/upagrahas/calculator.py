from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from datetime import timedelta
import swisseph as swe

class UpagrahaCalculator:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def normalize(self, deg):
        return deg % 360
        
    def calculate_upagrahas(self, date, lat, lon):
        """
        Calculates 5 Math Points + Gulika, Mandi, Yamaghantaka.
        """
        # 1. Get Sun Position
        sun_lon, _, _, _ = self.ep.get_planet_data(date, 'Sun')
        if sun_lon is None: return {}
        
        # 2. Mathematical Points
        dhuma = self.normalize(sun_lon + 133.3333) # 133 deg 20 min
        vyatipata = self.normalize(360 - dhuma)
        parivesha = self.normalize(vyatipata + 180)
        indrachapa = self.normalize(360 - parivesha)
        upaketu = self.normalize(indrachapa + 16.6666) # 16 deg 40 min
        
        # 3. Time-Based Points (Gulika, Mandi, Yamaghantaka)
        # Need Rise/Set
        rise_jd, set_jd = self.ep.get_sunrise_sunset(date, lat, lon)
        if rise_jd is None: return {} # Polar/Error
        
        current_jd = self.ep.get_julian_day(date)
        
        # Determine if Day or Night
        is_day = (current_jd >= rise_jd) and (current_jd < set_jd)
        
        # Duration
        if is_day:
            duration_days = set_jd - rise_jd
            start_jd = rise_jd
        else:
            # Night duration? 
            # If current_jd > set_jd, night is set_jd to next_rise_jd.
            # If current_jd < rise_jd, night is prev_set_jd to rise_jd.
            # Simplification: Assume standard day Cycle.
            # Ideally calculate next rise.
            # For robustness, let's approx night length as (1 - day_length) if calculating strictly.
            # Or fetch next rise.
            # Let's rely on day_length for Segment length calculation roughly or fetch next.
            # We'll use day duration logic for now as primarily markets are day.
            # But Upagrahas exist at night.
            # Let's compute 'duration' of the relevant segment.
            
            # If we are post-sunset:
            if current_jd >= set_jd:
                # Find NEXT rise
                 next_rise, _ = self.ep.get_sunrise_sunset(date + timedelta(days=1), lat, lon)
                 if next_rise:
                     duration_days = next_rise - set_jd
                     start_jd = set_jd
                 else:
                     duration_days = 0.5 # Fallback
                     start_jd = set_jd
            else:
                # Pre-sunrise (early morning)
                # Need Prev Set
                 curr_day_rise = rise_jd
                 prev_rise, prev_set_jd = self.ep.get_sunrise_sunset(date - timedelta(days=1), lat, lon)
                 if prev_set_jd:
                     duration_days = curr_day_rise - prev_set_jd
                     start_jd = prev_set_jd
                 else:
                     duration_days = 0.5
                     start_jd = current_jd - 0.2
        
        # Segment Logic (8 parts)
        part_len = duration_days / 8.0
        
        # Ruler Segments
        # Weekday (0=Mon, ... 6=Sun) -> Python weekday()
        # Vedic: 0=Sun (Sunday), 1=Moon... 6=Saturn.
        # Python: 0=Mon, 6=Sun. 
        # Convert Python to Vedic: (wd + 1) % 7? 
        # Mon(0)->Moon(1). Tue(1)->Mars(2). ... Sun(6)->Sun(0)? No.
        # Vedic map: Sun(0), Mon(1), Mars(2), Merc(3), Jup(4), Ven(5), Sat(6).
        # Python: Mon(0), Tue(1), Wed(2), Thu(3), Fri(4), Sat(5), Sun(6).
        # Map:
        py_wd = date.weekday()
        vedic_wd_map = {
            0: 1, # Mon -> Moon
            1: 2, # Tue -> Mars
            2: 3, # Wed -> Merc
            3: 4, # Thu -> Jup
            4: 5, # Fri -> Ven
            5: 6, # Sat -> Sat
            6: 0  # Sun -> Sun
        }
        day_lord = vedic_wd_map[py_wd]
        
        # Sequence: Sun(0), Moon(1), Mars(2), Merc(3), Jup(4), Ven(5), Sat(6)
        # Day Start: Day Lord.
        # Night Start: 5th from Day Lord. (Lord + 4) % 7
        
        start_idx = day_lord if is_day else (day_lord + 4) % 7
        
        # Find Segments for Saturn (Gulika/Mandi) and Jupiter (Yamaghantaka)
        # We need the START time of the Saturn/Jupiter segment.
        
        # Target Indices:
        # Saturn = 6
        # Jupiter = 4
        
        # Find which segment number (0-7) corresponds to Saturn/Jupiter
        # The sequence cycles 7 planets. The 8th segment is "Lordless" (or Rahu).
        # Sequence: start, start+1... 
        
        gulika_seg = -1
        yama_seg = -1
        
        for i in range(7):
            current_planet = (start_idx + i) % 7
            if current_planet == 6: # Saturn
                gulika_seg = i
            if current_planet == 4: # Jupiter
                yama_seg = i
                
        # Calculate Times
        # Gulika Time = Start + (gulika_seg * part_len)
        gulika_jd = start_jd + (gulika_seg * part_len)
        
        # Mandi Time
        # Mandi definition usually: Rises at start? Or Middle?
        # BPHS: "Gulika is at the beginning of Saturn's portion. Mandi is ???"
        # Standard software often treats them close. 
        # Some say Mandi rises at "Mandi Time".
        # Let's use the standard "Start of Segment" for Gulika.
        # And "Middle of Segment"? Or same?
        # Let's implement Gulika as Start.
        
        yama_jd = start_jd + (yama_seg * part_len)
        
        # Now we need the ASCENDANT at that specific JD.
        # EphemerisProvider get_houses takes 'date'. Need to convert JD to date or support JD.
        # Creating simple date object from JD is hard without conversion utils.
        # swe.revjul can convert JD to year, month, day, hour.
        
        def get_lagna_at_jd(target_jd):
            y, m, d, h = swe.revjul(target_jd)
            # h is decimal hours.
            # Construct datetime? Or just pass directly if get_houses supported JD?
            # get_houses takes date object to call get_julian_day.
            # But we can call swe.houses directly with JD.
            cusps, ascmc = swe.houses(target_jd, lat, lon, b'P')
            return ascmc[0]
            
        gulika_lon = get_lagna_at_jd(gulika_jd)
        yama_lon = get_lagna_at_jd(yama_jd)
        
        # Mandi: Often treated as distinct but similar. 
        # Let's compute Mandi as "Middle of Saturn Segment" for distinction.
        mandi_jd = gulika_jd + (part_len / 2.0)
        mandi_lon = get_lagna_at_jd(mandi_jd)

        return {
            'Dhuma': dhuma,
            'Vyatipata': vyatipata,
            'Parivesha': parivesha,
            'Indrachapa': indrachapa,
            'Upaketu': upaketu,
            'Gulika': gulika_lon,
            'Mandi': mandi_lon,
            'Yamaghantaka': yama_lon
        }
