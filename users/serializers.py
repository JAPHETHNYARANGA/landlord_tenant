from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Admin, Landlord, Tenant
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'surname', 'phone_number', 'email', 'dob', 'is_active', 'is_superuser', 'is_defaultpassword', 'role', 'is_staff', 'password', 'date_created']

    def create(self, validated_data):
        # Ensure password is hashed before saving
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # Ensure password is hashed before updating
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

# Admin Serializer
class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # Check if 'password' is in the user_data and handle it
        password = user_data.pop('password', None)
        user_data['is_superuser'] = True
        user = User(**user_data)
        
        # If password is provided, set it using set_password to ensure hashing
        if password:
            user.set_password(password)
        
        user.save()

        # Create the admin instance linked to the user
        admin = Admin.objects.create(user=user, **validated_data)
        return admin

# Landlord Serializer
class LandlordSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Landlord
        fields = ['user', 'government_id', 'dob', 'nationality']  # Ensure 'dob' is included here

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        role = user_data.get('role', 'LANDLORD').upper()
        user_data['role'] = role

        # Create the user
        user_data['is_staff'] = True  # Ensure the tenant's user is active
        user = User(**user_data)
        user.set_password(user_data['password'])
        user.save()

        # Create the landlord
        landlord = Landlord.objects.create(user=user, **validated_data)
        return landlord




class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tenant
        fields = ['user', 'government_id', 'nationality', 'house_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # Check if the user with the given email already exists
        if User.objects.filter(email=user_data['email']).exists():
            raise serializers.ValidationError({"email": "User with this email already exists."})

        # Create the user and set is_active to True
        user_data['is_active'] = True  # Ensure the tenant's user is active
        user = User(**user_data)
        user.set_password(user_data['password'])  # Hash the password
        user.save()

        # Ensure that the tenant's data is correctly passed and linked
        tenant_data = {
            'government_id': validated_data.get('government_id'),
            'nationality': validated_data.get('nationality'),
            'house_number': validated_data.get('house_number'),
            'user': user
        }
        tenant = Tenant.objects.create(**tenant_data)
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
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        data['user'] = user
        return data