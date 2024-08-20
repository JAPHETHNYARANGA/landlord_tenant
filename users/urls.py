from django.urls import path
from . import views  

urlpatterns = [
    # Admin endpoints
    path('create_admin/', views.create_admin, name='create_admin'),
    path('list_admins/', views.list_admins, name='list_admins'),
    path('update_admins/<int:admin_id>/', views.update_admins, name='update_admins'),
    path('delete_admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),

    # Tenant endpoints
    path('create_tenant/', views.create_tenant, name='create_tenant'),
    path('update_tenant/<int:tenant_id>/', views.update_tenant, name='update_tenant'),
    path('delete_tenant/<int:tenant_id>/', views.delete_tenant, name='delete_tenant'),
    path('list_tenants/', views.list_tenants, name='list_tenants'),
    
    

    # Landlord endpoints
    path('create_landlord/', views.create_landlord, name='create_landlord'),
    path('update_landlord/<int:landlord_id>/', views.update_landlord, name='update_landlord'),
    path('delete_landlord/<int:landlord_id>/', views.delete_landlord, name='delete_landlord'),
    path('list_landlords/', views.list_landlord, name='list_landlord'),
]
