from django.conf import settings
from django.db import models

from systeme.models import SystemeType

class Groupe(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Sous_groupe(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Equipement(models.Model):
    nom = models.CharField(max_length=100)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    sous_groupe = models.ForeignKey(Sous_groupe, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.CharField(max_length=20)
   # systemtype = models.ForeignKey(SystemeType, on_delete=models.CASCADE, related_name='systemtype_equipement_lies', default=1)

    def __str__(self):
        return f"{self.nom} ({self.unite})"

