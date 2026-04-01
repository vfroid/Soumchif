# calorifu/urls.py
from django.urls import path
import calorifu.views

app_name = "calorifu"

urlpatterns = [
    path('list/', calorifu.views.list, name='calorifu_list'),
    path('<int:pk>/new/', calorifu.views.new, name='calorifu_new'),
    path('<int:pk>/edit/', calorifu.views.edit, name='calorifu_edit'),
    path('<int:pk>/show/', calorifu.views.show, name='calorifu_show'),
    path('<int:pk>/delete/', calorifu.views.delete, name='calorifu_delete'),
    path('articles/<int:systeme_id>/', calorifu.views.articles_par_systeme, name='articles_par_systeme'),
]