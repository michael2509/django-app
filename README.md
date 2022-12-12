## Lancer le projet  

Notre library-project possède plusieurs apps (principe django)
Les relations entre les modèles de bdd (ou entités) doivent être définies que d'un côté de la relation

Cloner le projet
```console
git clone git@github.com:michael2509/django-app.git
```

```console
cd django-app/
```

Lancer le projet
```console
docker-compose up
```

Initialiser la base de donnée
```console
docker-compose exec web python manage.py migrate
```

Créer l'utilisateur admin
```console
docker-compose exec web python manage.py createsuperuser
```

Open browser in http://localhost:8000/admin