from django.urls import path
from .views import creating_booking, delete_booking, list_bookings, update_bookings


urlpatterns = [
    path('creating_booking/', creating_booking, name="creating_booking"),
    path('list_bookings/', list_bookings, name="list_booking"),
    path('update_booking/<int:booking_id>/', update_bookings, name="update_bookings"),
    path('delete_booking/<int:booking_id>/', delete_booking, name="delete_booking"),


    


]