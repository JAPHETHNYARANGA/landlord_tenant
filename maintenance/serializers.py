from rest_framework import serializers
from .models import MaintenanceTicket

class MaintenanceTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceTicket
        fields = ['ticket_id', 'tenant_id', 'property_id', 'issue_type', 'description', 'status', 'released_date', 'resolved_date']
