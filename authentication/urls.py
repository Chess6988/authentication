from django.urls import path
from .views import signup, signin, dashboard, activate_account, home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', dashboard, name='dashboard'),  # Set the dashboard view as the root URL
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('home/', home, name='home'),  # You can still keep the home view accessible via '/home/'
    path('activate/<int:pk>/', activate_account, name='activate_account'),
    
    # Add the logout URL
    path('logout/', LogoutView.as_view(next_page='signin'), name='logout'),
]
