Il faut rajouter un fichier .env:
    ``DJANGO_DB_NAME=XXXXXX
    DJANGO_DB_USER=XXXXXX
    DJANGO_DB_PASSWORD=XXXXXX
    DJANGO_DB_HOST=XXXXXX
    DJANGO_DB_PORT=XXXX``


Pour l'utilisation de make:
- make (lancer le projet)
- make migrate (lancer les migrations)
- make createsuperuser (création d'un user admin)