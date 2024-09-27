from django.db import models

class MonthlyDeduction(models.Model):
    date = models.DateField(auto_now_add=True)
    owner_salary = models.DecimalField(max_digits=10, decimal_places=2)
    driver_salaries = models.DecimalField(max_digits=10, decimal_places=2)
    owner_misc_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    mechanic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    other_staff_expenses = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_monthly_deductions(self):
        return (self.owner_salary + self.driver_salaries + self.owner_misc_expenses +
                self.mechanic_salary + self.other_staff_expenses)

    def __str__(self):
        return f"Monthly deductions for {self.date} - Total: {self.total_monthly_deductions}"
