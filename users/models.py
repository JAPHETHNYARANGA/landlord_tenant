from django.db import models


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Landlord(models.Model):
    landlord_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    government_id = models.CharField(max_length=50)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tenant(models.Model):
    tenant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    government_id = models.CharField(max_length=50)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)
    house_number = models.IntegerField()

    def __str__(self):
        return self.name