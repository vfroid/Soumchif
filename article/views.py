from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import ArticleForm
from systeme.models import Systeme
from systeme.forms import ArticleSystemeFormSet

def attribuer_systemes(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    all_systemes = Systeme.objects.all()  # tous les systèmes pour POST
    filtered_systemes = all_systemes

    # Filtrage par nom
    nom = request.GET.get('nom')
    if nom:
        filtered_systemes = filtered_systemes.filter(nom__icontains=nom)

    if request.method == 'POST':
        form = ArticleSystemeForm(request.POST, instance=article)
        # 🔹 pour le POST, le queryset complet
        form.fields['systemes'].queryset = all_systemes

        if form.is_valid():
            form.save()
            return redirect('article_show', pk=article.pk)
    else:
        # initialisation pour GET avec filtres visibles
        form = ArticleSystemeForm(instance=article, systemes_queryset=filtered_systemes)

    return render(request, 'article/attribuer_systemes.html', {
        'article': article,
        'form': form,
        'nom': nom,
    })



#*********************************  CRUD ***************************************************************

def show(request, pk):
    article = get_object_or_404(Article, pk=pk)  # récupère l'équipement ou 404
    return render(request, 'article/show.html', {'article': article})

def new(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()  # crée le nouvel article
            return redirect('article_list')  # redirige vers la liste des équipements
    else:
        form = ArticleForm()  # formulaire vide

    return render(request, 'article/new.html', {'form': form})


def edit(request, pk):
    article = get_object_or_404(Article, pk=pk)  # récupère l'équipement ou 404
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)  # remplit le formulaire existant
        if form.is_valid():
            form.save()  # sauvegarde les modifications
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)  # formulaire pré-rempli

    return render(request, 'article/edit.html', {'form': form, 'article': article})

def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()  # supprime l'équipement
        return redirect('article_list')
    return render(request, 'article/delete.html', {'article': article})

def list(request):
    articles = Article.objects.all()
    return render(request,
                  'article/list.html',
                  {'articles': articles})

def list_articles(request):
    articles = Article.objects.all()
    return render(request, 'article/list_articles.html', {'articles': articles})
