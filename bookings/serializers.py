from  rest_framework import serializers
from .models  import Booking



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['booking_id','property_id','tenant_id','booking_date','status']