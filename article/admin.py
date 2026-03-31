from django.contrib import admin

from article.models import Article



class ArticleAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = ('systeme','equipement','qte') # liste les champs que nous voulons sur l'affichage de la liste


admin.site.register(Article,ArticleAdmin)