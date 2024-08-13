from django.db import models
from  users.models import Landlord








class Property(models.Model):


   NAME_CHOICES =[
   ('Apartment','Apartment'),
   ('House','House'),
   ('Condo','Condo'),
   ]






   STATUS_CHOICES = [
       (0, 'Available'),
       (1, 'Not available'),
   ]




   name = models.CharField(max_length=255)
   location = models.CharField(max_length=200)
   rooms  = models.IntegerField()
   price = models.IntegerField()
   type = models.CharField(max_length=50,choices=STATUS_CHOICES)
   status = models.IntegerField(choices=STATUS_CHOICES)
   landlord_id  = models.IntegerField(Landlord, on_delete=models.CASCADE) #The Foreignkey field in Property model references the Landlord model from users app






   def __str__(self):
       return f"{self.name} - {self.location}"