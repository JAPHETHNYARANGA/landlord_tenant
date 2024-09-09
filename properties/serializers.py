from rest_framework import serializers
from .models import Property
from users.models import Landlord




class PropertySerializer(serializers.ModelSerializer):
    landlord_id = serializers.PrimaryKeyRelatedField(queryset=Landlord.objects.all())


    class Meta:
        model = Property
        fields = ['id','name','location','rooms','price','type','status','landlord_id']


