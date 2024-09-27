from django.db import models
from camions.models import Truck  # Importation du modèle Truck

class DashboardSummary(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='dashboard_summaries')  # Relation avec Truck
    created_at = models.DateTimeField(auto_now_add=True) 
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Résumé du tableau de bord pour {self.truck.matriculation_number} le {self.date}"