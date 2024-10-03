from django.urls import path
from . import views

urlpatterns = [
    path('register_truck/', views.register_truck, name='register_truck'),
    path('register_truck_info/', views.register_truck_info, name='register_truck_info'),
    path('enter_truck_data/', views.enter_truck_data, name='enter_truck_data'),  # New URL for truck data entry
  
]
