from django.db import models

class JyotishCalculation(models.Model):
    """
    Header for a calculation event (Date/Time/Location).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    target_date = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    ayanamsa_id = models.CharField(max_length=50, default="SIDM_LAHIRI")

class JyotishPoint(models.Model):
    """
    Stores one of the 33 points (Planet, Lagna, Upagraha).
    """
    calculation = models.ForeignKey(JyotishCalculation, on_delete=models.CASCADE, related_name='points')
    
    # Identify the point
    name = models.CharField(max_length=50) # e.g., 'Sun', 'Ascendant', 'Gulika'
    point_type = models.CharField(max_length=20) # 'Planet', 'Lagna', 'Upagraha'
    
    # Position
    longitude = models.FloatField() # 0-360
    speed = models.FloatField(null=True, blank=True)
    is_retrograde = models.BooleanField(default=False)
    declination = models.FloatField(null=True, blank=True)
    
    # Nakshatra Mapping
    nakshatra_name = models.CharField(max_length=50)
    nakshatra_number = models.IntegerField() # 1-27
    pada = models.IntegerField() # 1-4
    ruler = models.CharField(max_length=50)
    
    # Koorma Chakra
    direction = models.CharField(max_length=50) # e.g., 'Center', 'North-East'
    
    def __str__(self):
        return f"{self.name} in {self.nakshatra_name} ({self.longitude:.2f})"
