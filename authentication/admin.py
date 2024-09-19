from django.contrib import admin
from django.contrib.auth.models import User

# Register User model with default delete behavior
admin.site.unregister(User)
admin.site.register(User)
