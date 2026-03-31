
from django.conf import settings
from django.db import models

from systeme.models  import Systeme,SystemeType
from equipement.models import Equipement


class Article(models.Model):
    systeme=models.ForeignKey(Systeme,on_delete=models.CASCADE, related_name='systeme_articles')
    equipement = models.ForeignKey(Equipement,on_delete=models.CASCADE, related_name='equipement_articles')
    qte = models.DecimalField(max_digits=10, decimal_places=2, default=0) # decimal pour mètres (m)

    @property
    def montant(self):
        return float(self.equipement.prix) * float(self.qte or 0)

    def __str__(self):
        return f"{self.equipement.nom} ({self.qte} {self.equipement.unite})"