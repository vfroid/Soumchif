from django import forms
from article.models import Article


class ArticleForm(forms.Form):
    equipement_id = forms.IntegerField(widget=forms.HiddenInput)
    nom = forms.CharField(disabled=True)
    groupe = forms.CharField(disabled=True)
    sous_groupe = forms.CharField(disabled=True)
    prix = forms.DecimalField(disabled=True)

    qte = forms.DecimalField(required=False)
    ajouter = forms.BooleanField(required=False)