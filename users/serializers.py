from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Admin, Landlord, Tenant

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
        user = User.objects.create(**user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        return admin

# Landlord Serializer
class LandlordSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Landlord
        fields = ['user', 'government_id', 'nationality']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        landlord = Landlord.objects.create(user=user, **validated_data)
        return landlord

# Tenant Serializer
class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tenant
        fields = ['user', 'government_id', 'nationality', 'house_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        tenant = Tenant.objects.create(user=user, **validated_data)
        return tenant
