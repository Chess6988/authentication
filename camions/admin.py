from django.contrib import admin

# Register your models here.
from .models import Truck, RubberTransport  # Import the new model

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('matriculation_number', 'created_at')  # Columns to display in the admin
    search_fields = ('matriculation_number',)  # Add search functionality



@admin.register(RubberTransport)
class RubberTransportAdmin(admin.ModelAdmin):
    list_display = ('truck', 'number_of_trucks', 'tons_of_rubber', 'price_per_ton', 'date', 'total_price')  # Columns to display
    search_fields = ('truck__matriculation_number',)  # Search by truck matriculation number
    list_filter = ('date', 'truck')  # Filters to apply on the right side

    def total_price(self, obj):
        return obj.total_price()  # Call the method to display total price
    total_price.short_description = 'Total Price'  # Set a short description for the column