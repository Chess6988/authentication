from django.urls import path
from .views import signup, signin, dashboard, activate_account, signup_success

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('dashboard/', dashboard, name='dashboard'),
    path('activate/<int:pk>/', activate_account, name='activate_account'),
    path('signup-success/', signup_success, name='signup_success'),
]
