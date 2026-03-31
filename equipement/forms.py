from django import forms
from .models import Equipement, Groupe, Sous_groupe

class EquipementForm(forms.ModelForm):

    class Meta:
        model = Equipement
        fields = ['nom', 'groupe', 'sous_groupe', 'prix','unite']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groupe'].queryset = Groupe.objects.all()
        self.fields['sous_groupe'].queryset = Sous_groupe.objects.all()
