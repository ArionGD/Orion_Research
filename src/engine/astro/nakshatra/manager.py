import importlib
import os
import pkgutil

class NakshatraManager:
    """
    Aggregates logic from all 27 Nakshatra sub-modules.
    """
    def __init__(self):
        self.modules = []
        self.load_modules()
        
    def load_modules(self):
        package_path = "src/engine/nakshatra"
        # Dynamic loading of all subdirectories
        try:
            # Assuming running from root
            root = os.getcwd()
            base = os.path.join(root, package_path)
            
            if not os.path.exists(base):
                return

            for item in os.listdir(base):
                item_path = os.path.join(base, item)
                if os.path.isdir(item_path) and not item.startswith('__'):
                    # It's a nakshatra folder (e.g., 01_ashwini)
                    try:
                        module_name = f"src.engine.nakshatra.{item}.logic"
                        mod = importlib.import_module(module_name)
                        
                        # Find the class (Assume naming convention or just grab the first class that ends in Logic)
                        for attr_name in dir(mod):
                            if attr_name.endswith('Logic') and attr_name != 'EphemerisProvider':
                                cls = getattr(mod, attr_name)
                                self.modules.append(cls())
                                break
                    except Exception as e:
                        print(f"Failed to load Nakshatra {item}: {e}")
                        
        except Exception as e:
            print(f"Error initializing Nakshatra Manager: {e}")

    def get_aggregated_stress(self, planet_positions):
        """
        Polls all 27 Nakshatras for stress signals.
        """
        total_stress = 0
        signals = []
        
        for n_logic in self.modules:
            # Each logic module might check different things
            # For now, we pass all positions
            # In future V3, we pass specific planet data
            try:
                # Iterate planets
                for planet, lon in planet_positions.items():
                    res = n_logic.calculate_stress({'Planet': planet, 'Longitude': lon})
                    if res > 0:
                        total_stress += res
                        signals.append(f"Nakshatra Stress: {n_logic.deity} ({res})")
            except:
                pass
                
        return total_stress, signals
