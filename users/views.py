from rest_framework import viewsets, permissions, generics
from .models import Admin, Landlord, Tenant
from .serializers import AdminSerializer, LandlordSerializer, TenantSerializer


# //Admin
class AdminViewSet(generics.ListCreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can access

class AdminViewSetRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can access


# Landlord
class LandlordViewSet(generics.ListCreateAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can access

class LandlordViewSetRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can access


# Tenant
class TenantViewSet(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can access

class TenantViewSetRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can access    