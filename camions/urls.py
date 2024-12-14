from django.urls import path
from . import views

urlpatterns = [
    path('register_truck/', views.register_truck, name='register_truck'),
    path('truck-information/', views.truck_information, name='truck_information'),
    path('registered-trucks/', views.list_registered_trucks, name='list_registered_trucks'),
    path('add_rubber_transport/<int:truck_id>/', views.add_rubber_transport, name='add_rubber_transport'),
]