from django.urls import path
from . import views

urlpatterns = [
    path('register_truck/', views.register_truck, name='register_truck'),
    path('truck-information/', views.truck_information, name='truck_information'),
    
]  
