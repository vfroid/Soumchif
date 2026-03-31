from django.shortcuts import render, redirect, get_object_or_404
from .models import Projet
from .forms import ProjetForm
from article.models import Article
from calorifu.models import Calorifu
from django.db.models.functions import Coalesce
from django.db.models import Sum, F, Value, DecimalField, IntegerField, Q, FloatField

# Liste des projets
def list(request):
    projets=Projet.objects.all()
    return render(request,'projet/list.html',{'projets':projets})


from collections import defaultdict

def show(request, pk):
    projet = get_object_or_404(Projet, pk=pk)

    systemes_data = []
    total_projet = 0

    # 🔹 Pour le tableau global
    articles_groupes = defaultdict(lambda: {
        'nom': '',
        'unite': '',
        'prix': 0,
        'qte_totale': 0,
        'montant_total': 0
    })

    for systeme in projet.systemes.all():
        articles = systeme.articles_systeme
        total_systeme = 0

        for article in articles:
            montant = article.montant
            total_systeme += montant
            total_projet += montant

            eq = article.equipement

            # 🔹 Regroupement
            articles_groupes[eq.id]['nom'] = eq.nom
            articles_groupes[eq.id]['unite'] = eq.unite
            articles_groupes[eq.id]['prix'] = eq.prix
            articles_groupes[eq.id]['qte_totale'] += article.qte
            articles_groupes[eq.id]['montant_total'] += montant

        systemes_data.append({
            'systeme': systeme,
            'articles': articles,
            'total': total_systeme
        })

    context = {
        'projet': projet,
        'systemes_data': systemes_data,
        'total_projet': total_projet,
        'articles_groupes': articles_groupes.values(),  # 👈 important
    }

    return render(request, 'projet/show.html', context)
# Ajouter un projet
def new(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projet_list')
    else:
        form = ProjetForm()
    return render(request, 'projet/new.html', {'form': form})

# Modifier un projet
def edit(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    if request.method == 'POST':
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            return redirect('projet_edit', pk=projet.pk)
    else:
        form = ProjetForm(instance=projet)
    return render(request, 'projet/edit.html', {'form': form})

# Supprimer un projet
def delete(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    if request.method == 'POST':
        projet.delete()
        return redirect('projet_list')
    return render(request, 'projet/delete.html', {'projet': projet})
