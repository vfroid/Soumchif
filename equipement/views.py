from django.shortcuts import render,redirect

from equipement.forms import EquipementForm
from equipement.models import Equipement,Groupe,Sous_groupe
from .forms import EquipementForm

def list(request):
    equipements = Equipement.objects.all()
    return render(request,'equipement/list.html',{'equipements':equipements})

def show(request,pk):
    equipement = Equipement.objects.get(pk=pk)
    return render(request,'equipement/show.html',{'equipement':equipement})

def new(request):
    form=EquipementForm()
    if request.method == 'POST':
        form = EquipementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipement_list')
    else:
        form = EquipementForm()
    return render(request,'equipement/new.html',{'form':form})

def edit(request,pk):
    equipement = Equipement.objects.get(pk=pk)
    if request.method == 'POST':
        form = EquipementForm(request.POST,instance=equipement)
        if form.is_valid():
            form.save()
            return redirect('equipement_list')
    else:
        form = EquipementForm(instance=equipement)
    return render(request,'equipement/edit.html',{'form':form, 'equipement':equipement })

def delete(request,pk):
    equipement = Equipement.objects.get(pk=pk)
    if request.method == 'POST':
        equipement.delete()
        return redirect('equipement_list')
    else:
        return render(request,'equipement/delete.html')
