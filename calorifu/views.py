
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import CalorifuForm, CalorifuEditForm
from .models import Calorifu
from article.models import Article
from systeme.models import Systeme
from projet.models import Projet


def new(request, pk):
    projet = get_object_or_404(Projet, pk=pk)

    form = CalorifuForm(request.POST or None, projet=projet)

    if form.is_valid():
        calorifu = form.save(commit=False)
        # pré-remplir tuy avec la qte de l'article
        if calorifu.article:
            calorifu.tuy = calorifu.article.qte or 0
        calorifu.save()
        return redirect("calorifu:calorifu_list")  # adapte selon ton nom d'URL

    return render(request, "calorifu/new.html", {
        "form": form,
        "projet": projet
    })


# API pour récupérer les articles d'un système (sous-groupe "Tuyau")
def articles_par_systeme(request, systeme_id):
    try:
        systeme = Systeme.objects.get(id=systeme_id)
        articles = systeme.systeme_articles.filter(
            equipement__sous_groupe__nom__icontains="Tuyau"
        )
        data = [
            {"id": a.id, "equipement_nom": a.equipement.nom, "qte": float(a.qte)}
            for a in articles
        ]
        return JsonResponse(data, safe=False)
    except Systeme.DoesNotExist:
        return JsonResponse([], safe=False)



def edit(request,pk):
    calorifu=get_object_or_404(Calorifu,pk=pk)
    if request.method == 'POST':
        form = CalorifuEditForm(request.POST, instance=calorifu)
        if form.is_valid():
            form.save()
            return redirect('calorifu:calorifu_list')
    else:
        form = CalorifuForm(instance=calorifu)
    return render(request, 'calorifu/edit.html', {'form': form, 'calorifu':calorifu})

def list(request):
    calorifus = Calorifu.objects.all()
    return render(request, 'calorifu/list.html', {'calorifus': calorifus})

def show(request, pk):
    calorifu = get_object_or_404(Calorifu, pk=pk)
    return render(request, 'calorifu/show.html', {'calorifu': calorifu})

def delete(request, pk):
    calorifu = get_object_or_404(Calorifu, pk=pk)
    if request.method == 'POST':
        calorifu.delete()  # supprime l'équipement
        return redirect('calorifu:calorifu_list')
    return render(request, 'calorifu/delete.html', {'calorifu': calorifu})



