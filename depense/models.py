from django.db import models
from camions.models import Truck  # Import the Truck model

class DailyExpense(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    driver_road_costs = models.DecimalField(max_digits=10, decimal_places=2)# Frais de route
    fuel_and_misc = models.DecimalField(max_digits=10, decimal_places=2) # Carburant
    other_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    oil_change = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Vidange
    maintenance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)# Maintainance
    driver_salary = models.DecimalField(max_digits=10, decimal_places=2) # Salaire Chauffeur

    @property
    def total_expense(self):
        return sum([self.driver_road_costs, self.fuel_and_misc, self.other_expenses or 0,
                    self.oil_change or 0, self.maintenance or 0, self.driver_salary])

    def __str__(self):
        return f"Expenses for {self.truck} on {self.date} - Total: {self.total_expense}"
