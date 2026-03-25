from src.engine.lagna.calculator import LagnaCalculator

class LagnaManager:
    """
    Manager to provide Special Lagna points to the main engine.
    """
    def __init__(self):
        self.calc = LagnaCalculator()
        
    def get_special_lagnas(self, date, lat=40.7128, lon=-74.0060):
        """
        Returns Special Lagnas.
        Result: {Ascendant, MC, Hora_Lagna, Ghatika_Lagna, Arudha_Lagna_Sign, ...}
        Default Coordinates: NYSE (New York) for now, as User context implies Financial Engine.
        """
        return self.calc.calculate_special_lagnas(date, lat, lon)
