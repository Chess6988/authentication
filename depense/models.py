from django.db import models
from category.models import Categorie  # Importer le modèle Categorie de l'app category
from budget.models import Budget  # Importer le modèle Budget de l'app budget

# Modèle pour les dépenses
class Depense(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)  # Montant de la dépense
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="depenses")  # Relation 1:N avec Categorie
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="depenses")  # Relation N:1 avec Budget
    date = models.DateField(auto_now_add=True)  # Date ajoutée automatiquement lors de la création de la dépense
    
    def __str__(self):
        return f"{self.montant} € dépensé le {self.date} dans {self.categorie.nom}"