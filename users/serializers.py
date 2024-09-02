from rest_framework import serializers
from .models import User, Admin, Landlord, Tenant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number', 'password', 'role']
    
    def validate_role(self, value):
        if value not in dict(User.ROLE_CHOICES).keys():
            raise serializers.ValidationError("Invalid role choice.")
        return value



class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name', 'phone_number', 'password', 'role']

    def validate_role(self, value):
        if value not in dict(User.ROLE_CHOICES).keys():
            raise serializers.ValidationError("Invalid role choice.")
        return value



class LandlordSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Landlord
        fields = ['user', 'government_id', 'dob', 'nationality']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'landlord'
        user = User.objects.create(**user_data)
        return Landlord.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        return super().update(instance, validated_data)




class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tenant
        fields = ['user','government_id', 'dob', 'nationality', 'house_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'tenant'
        user = User.objects.create(**user_data)
        return Tenant.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        return super().update(instance, validated_data)

