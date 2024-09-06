from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Enter an email address")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_admin = True
        user.is_active = True
        user.is_defaultpassword = False
        user.save(using=self._db)
        all_groups = Group.objects.all()
        for admin_group in all_groups:
            admin_group.user_set.add(user)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ("ADMIN", "ADMIN"),
        ("LANDLORD", "LANDLORD"),
        ("TENANT", "TENANT"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=500, unique=True)
    dob = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_defaultpassword = models.BooleanField(default=True)
    role = models.CharField(max_length=255, choices=USER_TYPES, blank=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.surname}"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin_profile')

    def __str__(self):
        return f"{self.user.first_name} {self.user.surname}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True

    class Meta:
        db_table = 'admins'


class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='landlord_profile')
    government_id = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.surname}"


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='tenant_profile')
    government_id = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    house_number = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.surname}"
