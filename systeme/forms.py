from django import forms
from django.forms import modelformset_factory
from systeme.models import Systeme
from equipement.models import Equipement
from article.models import Article
from batiment.models import Local
from projet.models import Projet

# Formulaire principal pour Systeme
class SystemeForm(forms.ModelForm):
    class Meta:
        model = Systeme
        fields = ['nom', 'abreviation', 'type', 'local', 'projet']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'abreviation': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'local': forms.Select(attrs={'class': 'form-select'}),
            'projet': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['local'].queryset = Local.objects.all()
        self.fields['projet'].queryset = Projet.objects.all()


# Formulaire pour ajouter un article depuis un équipement
class ArticleAjoutForm(forms.Form):
    equipement_id = forms.IntegerField(widget=forms.HiddenInput)
    nom = forms.CharField(disabled=True)
    groupe = forms.CharField(disabled=True)
    sous_groupe = forms.CharField(disabled=True)
    unite = forms.CharField(disabled=True)
    prix = forms.DecimalField(disabled=True)
    qte = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1.0'})
    )
    ajouter = forms.BooleanField(required=False)


# pour modifier des articles
class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['qte']
        widgets = {
            'qte': forms.NumberInput(attrs={'class': 'form-control', 'step': '1.0'})
        }


ArticleSystemeFormSet = modelformset_factory(
    Article,
    form=ArticleEditForm,  # ✅ ICI
    extra=0,
    can_delete=True  # 🔥 important pour supprimer
)