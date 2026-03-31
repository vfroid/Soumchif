from django.db import models

from systeme.models import Systeme
from article.models import Article

class Calorifu(models.Model):
    #m Tuy	Cds	Emb	Rob	m Isol	Cds	Emb	Rob	m Anti Feu	Cds	Emb	Rob	Lts/m	lts
    tuy=models.DecimalField(max_digits=10, decimal_places=2, default=0) # mètres (m)
    tuy_cds=models.PositiveIntegerField( default=0)
    tuy_emb= models.PositiveIntegerField(default=0)
    tuy_rob= models.PositiveIntegerField(default=0)
    isol_cds = models.PositiveIntegerField(default=0)
    isol_emb = models.PositiveIntegerField(default=0)
    isol_rob = models.PositiveIntegerField(default=0)
    antifeu_cds = models.PositiveIntegerField(default=0)
    antifeu_emb = models.PositiveIntegerField(default=0)
    antifeu_rob = models.PositiveIntegerField(default=0)
    systeme=models.ForeignKey(Systeme,default='', on_delete=models.CASCADE, related_name='systeme_calorifus')
    article=models.ForeignKey(Article, on_delete=models.CASCADE, related_name='calorifus')

    def __str__(self):
        return f"{self.article.nom} {self.tuy} (m)"