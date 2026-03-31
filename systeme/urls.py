from django.urls import path

import systeme.views



urlpatterns = [
    path('systeme/list', systeme.views.list, name='systeme_list'),
    path('systeme/new', systeme.views.new, name='systeme_new'),
    path('systeme/<int:pk>/show', systeme.views.show, name='systeme_show'),
    path('systeme/<int:pk>/edit', systeme.views.edit, name='systeme_edit'),
    path('systeme/<int:pk>/delete', systeme.views.delete, name='systeme_delete'),
    path('ajax/equipements/', systeme.views.get_equipements, name='ajax_equipements'),
   ]
