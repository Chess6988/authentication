from django.urls import path
from . import views

urlpatterns = [
    path('register_truck/', views.register_truck, name='register_truck'),
    path('register_truck_info/', views.register_truck_info, name='register_truck_info'),
  
]
