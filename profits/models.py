from django.db import models
from depense.models import DailyExpense  # Import DailyExpense from depenses
from deduction_mensuel.models import MonthlyDeduction  # Import MonthlyDeduction from deductions

class MonthlyProfit(models.Model):
    date = models.DateField(auto_now_add=True)
    total_margin = models.DecimalField(max_digits=15, decimal_places=2)
    monthly_deductions = models.DecimalField(max_digits=15, decimal_places=2)

    @property
    def profit(self):
        return self.total_margin - self.monthly_deductions

    @property
    def profit_percentage(self):
        return (self.profit / self.total_margin) * 100

    def __str__(self):
        return f"Profit for {self.date} - {self.profit} ({self.profit_percentage:.2f}%)"


class DailySummary(models.Model):
    truck = models.ForeignKey('camions.Truck', on_delete=models.CASCADE)  # Import Truck model
    date = models.DateField(auto_now_add=True)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2)

    @property
    def margin(self):
        return self.total_revenue - self.total_expenses

    def __str__(self):
        return f"Summary for {self.truck} on {self.date} - Margin: {self.margin}"
