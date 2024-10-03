from django.core.exceptions import ValidationError
import re
from django.db import models

class Truck(models.Model):
    matriculation_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Define the expected format: 2 letters, space, 4 digits, space, 1 letter
        if not re.match(r'^[A-Z]{2} \d{4} [A-Z]$', self.matriculation_number):
            raise ValidationError('Matriculation number must follow the format "LT 1234 M"')

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call clean() before saving to validate the format
        super().save(*args, **kwargs)

    def __str__(self):
        return self.matriculation_number


class RubberTransport(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    number_of_truck = models.IntegerField(default=1)
    tons_of_rubber = models.FloatField(default=0.0) 
    price_per_ton = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    @property
    def total_revenue(self):
        return self.tons_of_rubber * self.price_per_ton

    def __str__(self):
        return f"{self.truck} - {self.total_revenue} on {self.date}"
