import os

# Data for all 27 Nakshatras
# Name, Ruler, Deity, Description
nakshatra_data = [
    ("01_ashwini", "Ketu", "Ashwini Kumaras", "Speed, Healing, New Beginnings"),
    ("02_bharani", "Venus", "Yama", "Restraint, Death/Rebirth, Struggles"),
    ("03_krittika", "Sun", "Agni", "Fire, Purification, cutting ties"),
    ("04_rohini", "Moon", "Brahma", "Growth, Creativity, Desire"),
    ("05_mrigashira", "Mars", "Soma", "Searching, Restlessness, Deer Head"),
    ("06_ardra", "Rahu", "Rudra", "Storms, Destruction for Creation, Tears"),
    ("07_punarvasu", "Jupiter", "Aditi", "Return of the Light, Renewal"),
    ("08_pushya", "Saturn", "Brihaspati", "Nourishment, The Best Star, Legal"),
    ("09_ashlesha", "Mercury", "Nagas", "Serpent energy, Entanglement, Poison"),
    ("10_magha", "Ketu", "Pitris", "Ancestors, Authority, Throne"),
    ("11_purva_phalguni", "Venus", "Bhaga", "Enjoyment, Relaxation, Fruit"),
    ("12_uttara_phalguni", "Sun", "Aryaman", "Patronage, Kindness, Contracts"),
    ("13_hasta", "Moon", "Savitr", "The Hand, Skill, Manifestation"),
    ("14_chitra", "Mars", "Vishvakarma", "The Architect, Brilliance, Jewel"),
    ("15_swati", "Rahu", "Vayu", "The Wind, Independence, Scattering"),
    ("16_vishakha", "Jupiter", "Indra-Agni", "The Forked Branch, Purpose, Obsession"),
    ("17_anuradha", "Saturn", "Mitra", "Friendship, Devotion, Alliance"),
    ("18_jyeshtha", "Mercury", "Indra", "The Eldest, Seniority, Protection"),
    ("19_mula", "Ketu", "Nirriti", "The Root, Destruction, Calamity"),
    ("20_purva_ashadha", "Venus", "Apas", "Water, Invincibility, Purification"),
    ("21_uttara_ashadha", "Sun", "Vishveshvaras", "Universal Gods, Victory, Responsibility"),
    ("22_shravana", "Moon", "Vishnu", "Listening, Perception, Expansion"),
    ("23_dhanishta", "Mars", "Vasus", "Wealth, Fame, Music"),
    ("24_shatabhisha", "Rahu", "Varuna", "100 Physicians, Healing (or shielding)"),
    ("25_purva_bhadrapada", "Jupiter", "Aja Ekapada", "The One-Footed Goat, Sacrifice, Fire"),
    ("26_uttara_bhadrapada", "Saturn", "Ahir Budhnya", "Deep Water Serpent, Stability"),
    ("27_revati", "Mercury", "Pushan", "The Nourisher, Safe Journeys, Wealth")
]

base_path = "src/engine/nakshatra"

class_template = """from src.engine.astro.core.ephemeris_provider import EphemerisProvider

class {class_name}Logic:
    def __init__(self):
        self.ep = EphemerisProvider()
        self.ruler = "{ruler}"
        self.deity = "{deity}"
        self.description = "{description}"
        
    def calculate_stress(self, planet_data):
        # Placeholder for specific {name} logic
        # e.g., if Mars is in {name} and meets a specific Pada...
        return 0
"""

def create_scaffold():
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        
    for name, ruler, deity, desc in nakshatra_data:
        # Create Folder
        folder_path = os.path.join(base_path, name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        # Create logic.py
        file_path = os.path.join(folder_path, "logic.py")
        
        # Format Class Name (e.g. 01_ashwini -> Ashwini)
        # remove number prefix
        clean_name = name.split('_', 1)[1].title().replace('_', '')
        
        content = class_template.format(
            class_name=clean_name,
            name=name,
            ruler=ruler,
            deity=deity,
            description=desc
        )
        
        with open(file_path, "w") as f:
            f.write(content)
            
        # Create __init__.py
        with open(os.path.join(folder_path, "__init__.py"), "w") as f:
            f.write("")
            
    print(f"Successfully created {len(nakshatra_data)} Nakshatra modules.")

if __name__ == "__main__":
    create_scaffold()
