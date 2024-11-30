from django.contrib import admin

# Register your models here.
from .models import Truck

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('matriculation_number', 'created_at')  # Columns to display in the admin
    search_fields = ('matriculation_number',)  # Add search functionality