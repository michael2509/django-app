## Lancer le projet  

Règle les problème de permissions
```console
foo@bar:~$ sudo chown -R $USER:$USER ./
```

Lancer le projet
```console
foo@bar:~$ docker-compose up
```

Initialiser la base de donnée
```console
foo@bar:~$ docker-compose exec web python manage.py makemigrations
```

```console
foo@bar:~$ docker-compose exec web python manage.py migrate
```

Open browser in http://localhost:8000/polls