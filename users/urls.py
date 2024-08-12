from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('admins/', views.AdminViewSet.as_view(), name="admin"),
    path('admins/<int:pk>/', views.AdminViewSetRetrieveUpdateDestroy.as_view(), name="update-admin"),

    path('landlords/', views.LandlordViewSet.as_view(), name="landlords"),
    path('landlords/<int:pk>/', views.LandlordViewSetRetrieveUpdateDestroy.as_view(), name="update-admin"),

    path('tenants/', views.TenantViewSet.as_view(), name="tenants"),
    path('tenants/<int:pk>/', views.TenantViewSetRetrieveUpdateDestroy.as_view(), name="update-admin"),
    
]
