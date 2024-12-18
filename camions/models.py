import re
from django.core.exceptions import ValidationError
from django.db import models
from decimal import Decimal

class Truck(models.Model):
    matriculation_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['matriculation_number', 'created_at'],
                name='unique_daily_matriculation'
            )
        ]

    def __str__(self):
        return self.matriculation_number



class RubberTransport(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name="rubber_transports")
    number_of_trucks = models.PositiveIntegerField(default=1)  # Ensures non-negative integers
    tons_of_rubber = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    price_per_ton = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def total_price(self):
        """Calculate the total price for the rubber transported."""
        return self.tons_of_rubber * self.price_per_ton

    def __str__(self):
        return f"Transport on {self.date} by {self.truck.matriculation_number}"