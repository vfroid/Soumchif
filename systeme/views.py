# systeme/views.py
from django.shortcuts import render, redirect, get_object_or_404
from systeme.models import SystemeType, Systeme
from equipement.models import Equipement
from article.models import Article
from .forms import SystemeForm
from article.forms import ArticleForm
from django.forms import modelformset_factory

from .forms import (
    SystemeForm,
    ArticleAjoutForm,
    ArticleEditForm,
    ArticleSystemeFormSet,
)

from django.http import JsonResponse


def get_equipements(request):
    type_id = request.GET.get('type_id')
    data = []

    if type_id:
        try:
            type_obj = SystemeType.objects.get(pk=type_id)
            equipements = type_obj.equipements_lies.all()

            for e in equipements:
                data.append({
                    'id': e.id,
                    'nom': e.nom,
                    'groupe': e.groupe.nom,
                    'sous_groupe': e.sous_groupe.nom,
                    'unite': e.unite,
                    'prix': float(e.prix),
                })
        except SystemeType.DoesNotExist:
            pass

    return JsonResponse({'equipements': data})




#******************************************** CRUD *************************************************/
def list(request):
    systemes=Systeme.objects.all()
    return render(request,'systeme/list.html', {'systemes': systemes })

def show(request, pk):
    systeme = get_object_or_404(Systeme, pk=pk)

    # uniquement les articles liés
    articles = systeme.articles.all()

    # total (optionnel mais utile)
    total = sum(a.montant for a in articles)

    return render(request, "systeme/show.html", {
        "systeme": systeme,
        "articles": articles,
        "total":total,
    })



def new(request):
    form = SystemeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        systeme = form.save()

        i = 0
        while True:
            prefix = f'add-{i}-'
            if prefix + 'equipement_id' not in request.POST:
                break

            ajouter = request.POST.get(prefix + 'ajouter')
            equipement_id = request.POST.get(prefix + 'equipement_id')
            qte = request.POST.get(prefix + 'qte') or 0

            if ajouter:
                Article.objects.create(
                    systeme=systeme,
                    equipement_id=equipement_id,
                    qte=qte
                )

            i += 1

        return redirect('systeme_list')

    return render(request, 'systeme/new.html', {
        'form': form
    })


def edit(request, pk):
    systeme = get_object_or_404(Systeme, pk=pk)
    form = SystemeForm(request.POST or None, instance=systeme)

    # 🔹 ARTICLES EXISTANTS
    articles_existants = Article.objects.filter(systeme=systeme)
    articles_existants_forms = []

    # Construire un formulaire pour chaque article existant
    for i, art in enumerate(articles_existants):
        articles_existants_forms.append(
            ArticleAjoutForm(
                request.POST if request.method == 'POST' else None,
                prefix=f'exist-{i}',
                initial={
                    'equipement_id': art.equipement.id,
                    'nom': art.equipement.nom,
                    'groupe': art.equipement.groupe.nom,
                    'sous_groupe': art.equipement.sous_groupe.nom,
                    'unite': art.equipement.unite,
                    'prix': art.equipement.prix,
                    'qte': art.qte,
                    'ajouter': True,
                }
            )
        )

    # 🔹 NOUVEAUX EQUIPEMENTS
    equipements_nouveaux = systeme.type.equipements_lies.exclude(
        id__in=[a.equipement.id for a in articles_existants]
    )
    articles_nouveaux_forms = []
    for i, e in enumerate(equipements_nouveaux):
        articles_nouveaux_forms.append(
            ArticleAjoutForm(
                request.POST if request.method == 'POST' else None,
                prefix=f'new-{i}',
                initial={
                    'equipement_id': e.id,
                    'nom': e.nom,
                    'groupe': e.groupe.nom,
                    'sous_groupe': e.sous_groupe.nom,
                    'unite': e.unite,
                    'prix': e.prix,
                    'qte': 0,
                    'ajouter': False
                }
            )
        )

    # 🔹 POST : sauvegarde
    if request.method == 'POST' and form.is_valid():
        systeme = form.save()

        # Articles existants : mise à jour des qte
        for f in articles_existants_forms:
            if f.is_valid():
                equipement_id = f.cleaned_data['equipement_id']
                qte = f.cleaned_data.get('qte') or 0
                article = Article.objects.get(systeme=systeme, equipement_id=equipement_id)
                article.qte = qte
                article.save()

        # Nouveaux articles : création si checkbox cochée
        for f in articles_nouveaux_forms:
            if f.is_valid() and f.cleaned_data.get('ajouter'):
                equipement_id = f.cleaned_data['equipement_id']
                qte = f.cleaned_data.get('qte') or 0
                # éviter doublon
                if not Article.objects.filter(systeme=systeme, equipement_id=equipement_id).exists():
                    Article.objects.create(systeme=systeme, equipement_id=equipement_id, qte=qte)

        return redirect('systeme_list')

    return render(request, 'systeme/edit.html', {
        'form': form,
        'articles_existants_forms': articles_existants_forms,
        'articles_nouveaux_forms': articles_nouveaux_forms,
        'systeme': systeme,
    })


def delete(request, pk):
    systeme = get_object_or_404(Systeme, pk=pk)

    if request.method == "POST":
        systeme.delete()
        return redirect("systeme_list")

    return render(request, "systeme/delete.html", {"systeme": systeme})