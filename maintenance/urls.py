from django.urls import path
from .views import create_maintenance_ticket,list_tickets, update_ticket

urlpatterns = [
    path('create_maintenance_ticket/', create_maintenance_ticket, name='create_maintenance_ticket'),
    path('list_tickets/', list_tickets, name='list_tickets'),
    path('update_ticket/<int:ticket_id>/', update_ticket, name="update_ticket")
]
