# Installation et configuration du projet Django

Ce guide explique comment initialiser et configurer le projet Django `Soumchif`.


## Initialisation du projet

Dans le dossier du projet, exécutez les commandes suivantes :

```bash
# Initialiser Git
git init

# Créer un environnement virtuel
python3 -m venv env

# Activer l'environnement virtuel
source env/bin/activate

# Installer Django
pip install django

# Générer le fichier des dépendances
pip freeze > requirements.txt

# Créer le projet Django
django-admin startproject soumchif

# Appliquer les migrations initiales
python manage.py migrate

# Créer un superutilisateur pour l'administration
python manage.py createsuperuser
```
## Remplissage de la base de données
Les données peuvent être insérées en base de données via le fichier Remplissage_BDD.odt.
Pour les bâtiments, importer les données de locauxminimum.csv dans la table batiment_local via le prompt de sqlite3 ouvert via 

puis

```bash
python manage.py dbshell
.separator ','
.import locauxminmum.csv batiment_local
```
## Lancer le serveur local
```bash
python manage.py runserver
