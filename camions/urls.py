from django.urls import path
from . import views

urlpatterns = [
    path('register_truck/', views.register_truck, name='register_truck'),
    path('truck-information/', views.truck_information_view, name='truck_information'),
    path('truck-data-form/', views.truck_data_form_view, name='truck_data_form'),
]  
