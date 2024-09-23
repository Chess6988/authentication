from django.db import models
from category.models import Categorie  # Importer le modèle Categorie de l'app category

# Modèle pour les budgets
class Budget(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)  # Montant du budget
    categorie = models.OneToOneField(Categorie, on_delete=models.CASCADE, related_name="budget")  # Relation 1:1 avec Catégorie
    date = models.DateField(auto_now_add=True)  # Date ajoutée automatiquement lors de la création du budget
    
    def __str__(self):
        return f"Budget pour {self.categorie.nom} : {self.montant} €"