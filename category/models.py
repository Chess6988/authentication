from django.db import models

# Modèle pour les catégories (ex: Alimentation, Transport, Santé)
class Categorie(models.Model):
    nom = models.CharField(max_length=100)  # Nom de la catégorie (Alimentation, Transport, etc.)
    
    def __str__(self):
        return self.nom