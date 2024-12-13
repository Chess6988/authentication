import re
from django.core.exceptions import ValidationError
from django.db import models

class Truck(models.Model):
    matriculation_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.matriculation_number


class RubberTransport(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    number_of_truck = models.IntegerField(default=1)
    tons_of_rubber = models.FloatField(default=0.0) 
    price_per_ton = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f'Truck: {self.truck}, Tons of Rubber: {self.tons_of_rubber}, Date: {self.date}'
