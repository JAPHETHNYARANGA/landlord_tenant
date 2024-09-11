
from django.db import models  
from properties.models import Property
from users.models import Tenant




class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled'),
        
        ('Completed', 'Completed'),
    ]



    booking_id = models.AutoField(primary_key=True)
    property_id  = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant_id  = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    booking_date  = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')

    def __str_(self):
        return f"Booking {self.booking_id}:{self.status}"