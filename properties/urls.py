from django.urls import path
from . import views  
urlpatterns = [
    path('create_property/', views.create_property, name='create_property'),  
    path('list_property/', views.list_property, name='list_property'),
    path('update_property/<int:id>/', views.update_property, name='update_property'),  
    path('delete_property/<int:id>/', views.delete_property, name='delete_property'),  


]
