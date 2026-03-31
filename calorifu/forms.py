from django import forms
from .models import Calorifu

class CalorifuForm(forms.ModelForm):
    class Meta:
        model = Calorifu
        fields = [
            'tuy', 'tuy_cds', 'tuy_emb', 'tuy_rob',
            'isol_cds', 'isol_emb', 'isol_rob',
            'antifeu_cds', 'antifeu_emb', 'antifeu_rob',
            'systeme','article'
        ]
        labels = {
            'tuy': 'Mètres (m) Tuyaux',
            'tuy_cds': 'CDS Tuyaux',
            'tuy_emb': 'Embouts Tuyaux',
            'tuy_rob': 'Robinetterie Tuyaux',
            'isol_cds': 'CDS Isolation',
            'isol_emb': 'Embouts Isolation',
            'isol_rob': 'Robinetterie Isolation',
            'antifeu_cds': 'CDS Anti-Feu',
            'antifeu_emb': 'Embouts Anti-Feu',
            'antifeu_rob': 'Robinetterie Anti-Feu',
            'systeme':'Systeme',
            'article': 'Article',
        }
        widgets = {
            'tuy': forms.NumberInput(attrs={'step': '0.01'}),
            'systeme': forms.Select(attrs={'class': 'form-control'}),
            'article': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Vous pouvez ajouter ici des personnalisations supplémentaires si nécessaire
