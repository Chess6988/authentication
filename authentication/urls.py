from django.urls import path
from .views import signup, signin, dashboard, activate_account, home  # Import the home view

urlpatterns = [
    path('', home, name='home'),  # Set the home view as the root URL
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('dashboard/', dashboard, name='dashboard'),
    path('activate/<int:pk>/', activate_account, name='activate_account'),
]
