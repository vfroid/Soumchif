from django.db import models
from batiment.models import Local
from projet.models import Projet
from django.db.models import Sum, F

class SystemeType(models.Model):
    # Nom et abréviation
    nom = models.CharField(max_length=100)
    abreviation = models.CharField(max_length=10, blank=True, null=True)

    # Choix Production / Emission
    PRODUCTION = 'PROD'
    EMISSION = 'EMI'
    PRODOUEMIS_CHOICES = [
        (PRODUCTION, 'Production'),
        (EMISSION, 'Emission'),
    ]
    prodouemis = models.CharField(
        max_length=4,
        choices=PRODOUEMIS_CHOICES,
        default=PRODUCTION,
        verbose_name="Type"
    )

    # Articles liés
    equipements_lies = models.ManyToManyField(
        'equipement.Equipement',  # référence par string pour éviter circular import
        related_name='systeme_types',
        blank=True
    )

    def __str__(self):
        return f"{self.nom} ({self.abreviation or ''}) - {self.get_prodouemis_display()}"



class Systeme(models.Model):
    nom = models.CharField(max_length=100)
    abreviation = models.CharField(max_length=30, blank=True, null=True)

    # Référence au type de système
    type = models.ForeignKey(
        'systeme.SystemeType',  # référence par string pour éviter circular import
        on_delete=models.CASCADE,
        related_name='systemes'
    )

    # Optionnel : local et projet
    local = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        related_name='systemes',
        null=True,
        blank=True
    )
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name='systemes'
    )

    # Articles attribués au système
    articles = models.ManyToManyField(
        'article.Article',
        related_name='systemes_lies',
        blank=True
    )

    def __str__(self):
        return f"{self.nom} ({self.abreviation or ''}) - {self.projet.mandant}"

    @property
    def articles_systeme(self):
        """Articles liés au système avec qte > 0"""
        return self.articles.filter(qte__gt=0)

    def get_articles_proposes(self):
        """Retourne les articles proposés par le SystemeType si le système est vide"""
        if not self.articles.exists():
            return self.type.articles_lies.all()
        return self.articles_systeme

    def montant_total_articles(self):
        #"""Montant total des articles du système"""
        #return self.articles_systeme.aggregate(total=models.Sum('montant'))['total'] or 0
        return self.articles_systeme.aggregate(
                total=Sum(F('prix') * F('qte'))
            )['total'] or 0

    def ajouter_articles(self, articles):
        """Ajoute au système les articles avec qte > 0"""
        for article in articles:
            if article.qte > 0:
                self.articles.add(article)