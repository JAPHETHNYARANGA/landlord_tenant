from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Creating profile based on user role
        if role == 'admin':
            Admin.objects.create(user=user)
        elif role == 'landlord':
            Landlord.objects.create(user=user)
        elif role == 'tenant':
            Tenant.objects.create(user=user)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, 'admin', password, **extra_fields)

class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin_profile')

    def __str__(self):
        return self.user.name


class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='landlord_profile')
    government_id = models.CharField(max_length=50)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='tenant_profile')
    government_id = models.CharField(max_length=50)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)
    house_number = models.IntegerField()

    def __str__(self):
        return self.user.name
