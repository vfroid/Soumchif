from django.urls import path,include

import equipement.views

urlpatterns = [
    path('equipement/list', equipement.views.list,name='equipement_list'),
    path('equipement/<int:pk>/show', equipement.views.show,name='equipement_show'),
    path('equipement/new', equipement.views.new,name='equipement_new'),
    path('equipement/<int:pk>/edit', equipement.views.edit, name='equipement_edit'),
    path('equipement/<int:pk>/delete', equipement.views.delete, name='equipement_delete'),
]