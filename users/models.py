from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Enter an email address")
        
        # Create user instance
        user = self.model(email=self.normalize_email(email), **extra_fields)
        
        # Hash the password using set_password
        user.set_password(password)
        
        # Save user in the database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)  # Ensure superuser is active
        extra_fields.setdefault('role', 'ADMIN')  # Assign the admin role
        
        return self.create_user(email=email, password=password, **extra_fields)

    def create_admin(self, email, password=None, **extra_fields):
        """Create an admin user."""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)  # Ensure admin is active
        
        # Set the role to 'ADMIN'
        extra_fields['role'] = "ADMIN"
        
        return self.create_user(email=email, password=password, **extra_fields)

    def create_landlord(self, email, password=None, **extra_fields):
        """Create a landlord user."""
        extra_fields.setdefault('is_staff', True)  # Set is_staff to True for landlords
        extra_fields.setdefault('is_active', True)  # Ensure landlord is active (changed to True)
        extra_fields.setdefault('role', 'LANDLORD')  # Automatically assign the 'LANDLORD' role
        
        # Create the user
        return self.create_user(email=email, password=password, **extra_fields)

    def create_tenant(self, email, password=None, **extra_fields):
        """Create a tenant user."""
        extra_fields.setdefault('is_staff', False)  # Set is_staff to False for tenants
        extra_fields.setdefault('is_active', True)  # Ensure tenant is active
        extra_fields.setdefault('role', 'TENANT')  # Automatically assign the 'TENANT' role
        
        # Create the user
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ("ADMIN", "ADMIN"),
        ("LANDLORD", "LANDLORD"),
        ("TENANT", "TENANT"),
    ]
    
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    dob = models.DateField(null=True, blank=True)  # Changed to DateField to match payload format
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_defaultpassword = models.BooleanField(default=True)
    role = models.CharField(max_length=255, choices=USER_TYPES, blank=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set the current date and time when creating a user

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
    dob = models.DateField(null=True, blank=True)
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


