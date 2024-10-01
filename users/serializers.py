from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Admin, Landlord, Tenant
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    is_active = serializers.BooleanField(default=True)  # Ensure the default is True

    class Meta:
        model = User
        fields = ['id', 'first_name', 'surname', 'phone_number', 'email', 'dob', 
                  'is_active', 'is_superuser', 'is_defaultpassword', 'role', 'is_staff', 'password', 'date_created']

    def create(self, validated_data):
        # Ensure the password is hashed before saving
        validated_data['password'] = make_password(validated_data.get('password'))

        # Ensure is_active is passed and defaults to True if not provided
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
        
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        return super(UserSerializer, self).update(instance, validated_data)


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        # Explicitly set is_active to True if not provided
        user_data.setdefault('is_active', True)
        
        password = user_data.pop('password', None)
        user_data['is_superuser'] = True
        user_data['is_staff'] = True

        user = User(**user_data)

        if password:
            user.set_password(password)

        user.save()

        admin = Admin.objects.create(user=user, **validated_data)
        return admin


class LandlordSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Landlord
        fields = ['user', 'government_id', 'dob', 'nationality']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # Explicitly set is_active to True if not provided
        user_data.setdefault('is_active', True)

        # Set role to LANDLORD
        user_data['role'] = 'LANDLORD'
        
        password = user_data.pop('password', None)
        user = User(**user_data)

        if password:
            user.set_password(password)

        user.save()

        landlord = Landlord.objects.create(user=user, **validated_data)
        return landlord

class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tenant
        fields = ['user', 'lease_start', 'lease_end', 'property_rented']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # Explicitly set is_active to True if not provided
        user_data.setdefault('is_active', True)

        # Set role to TENANT
        user_data['role'] = 'TENANT'
        
        password = user_data.pop('password', None)
        user = User(**user_data)

        if password:
            user.set_password(password)

        user.save()

        tenant = Tenant.objects.create(user=user, **validated_data)
        return tenant

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise serializers.ValidationError("Incorrect password.")
                if not user.is_active:  # Check if the user is active
                    raise serializers.ValidationError({"detail": "User is inactive", "code": "user_inactive"})
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        data['user'] = user
        return data




        