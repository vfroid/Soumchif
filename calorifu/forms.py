from django import forms
from .models import Calorifu
from systeme.models import Systeme
from article.models import Article

class CalorifuForm(forms.ModelForm):
    class Meta:
        model = Calorifu
        fields = [
            "systeme",
            "article",
            "tuy",
            "tuy_cds",
            "tuy_emb",
            "tuy_rob",
            "isol_cds",
            "isol_emb",
            "isol_rob",
            "antifeu_cds",
            "antifeu_emb",
            "antifeu_rob",
        ]

    def __init__(self, *args, **kwargs):
        projet = kwargs.pop("projet", None)
        super().__init__(*args, **kwargs)

        self.fields["systeme"].required = True
        self.fields["article"].required = True

        # filtrer les systèmes du projet
        if projet:
            self.fields["systeme"].queryset = projet.systemes.all()
        else:
            self.fields["systeme"].queryset = Systeme.objects.none()

        # déterminer le système choisi
        systeme_id = self.data.get("systeme") or getattr(self.instance, "systeme_id", None)
        if systeme_id:
            try:
                systeme = Systeme.objects.get(id=systeme_id)
                # filtrer les articles du sous-groupe "Tuyau"
                self.fields["article"].queryset = systeme.systeme_articles.filter(
                    equipement__sous_groupe__nom__icontains="Tuyau"
                )
            except Systeme.DoesNotExist:
                self.fields["article"].queryset = Article.objects.none()
        else:
            self.fields["article"].queryset = Article.objects.none()

        # pré-remplir tuy avec article.qte si disponible
        article_id = self.data.get("article") or getattr(self.instance, "article_id", None)
        if article_id:
            try:
                article = Article.objects.get(id=article_id)
                self.fields["tuy"].initial = article.qte
            except Article.DoesNotExist:
                self.fields["tuy"].initial = 0
        else:
            self.fields["tuy"].initial = 0

# calorifu/forms.py
class CalorifuEditForm(forms.ModelForm):
    class Meta:
        model = Calorifu
        fields = [
            "tuy",
            "tuy_cds",
            "tuy_emb",
            "tuy_rob",
            "isol_cds",
            "isol_emb",
            "isol_rob",
            "antifeu_cds",
            "antifeu_emb",
            "antifeu_rob",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('systeme', None)
        self.fields.pop('article', None)
