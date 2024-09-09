from django.db import models
from users.models import Landlord  # Importing the Landlord model from the users app

class Property(models.Model):
    NAME_CHOICES = [
        ('Apartment', 'Apartment'),
        ('House', 'House'),
        ('Condo', 'Condo'),
    ]
    
    STATUS_CHOICES = [
        (0, 'Available'),
        (1, 'Not available'),
    ]
    
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=200)
    rooms = models.IntegerField()
    price = models.IntegerField()
    type = models.CharField(max_length=50, choices=NAME_CHOICES)  
    status = models.IntegerField(choices=STATUS_CHOICES)
    landlord_id = models.ForeignKey(Landlord, on_delete=models.CASCADE)  

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name','rooms'], name='unique_property_name_rooms')

        ]
        #enforces that the combination of name and rooms must be unique
    def __str__(self):
        return f"{self.name} - {self.location}"
