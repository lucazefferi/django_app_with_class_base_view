Per far partire l'app recarsi in /todolistprj che è la cartella che contiene il manage.py 
e lanciare "python manage.py runserver"

quando si crea un nuovo modello per creare la tab bisogna lanciare il comanda "python manage.py makemigration" 
e poi "python manage.py migration"

Come creare un virtual environment, cosa utile per gestire il nostro progetto e non dover scaricare le dipendenze in locale
https://aulab.it/guide-avanzate/come-creare-un-virtual-environment-in-python

Se invece vogio far partire la mia app su docker devo:
Cosa è docker? ->  https://www.youtube.com/watch?v=ek6WanZKaDc

1) creare un requirements.txt che al suo interno avrà tutte le dipendenze e usate per il progetto posso,
per crearlo recarsi nelle dir del progetto (C:\myProject\python\DJANGO_APP\todolistprj) lanciare il comando:

pip freeze >requirements.txt (fa export di tutte le dipendenze nel file indicato)

2) Creare il dockerfile che contiene le informazioni per la creazione della nostra Img docker

3) Lanciare il comando:

docker build -t {inserire il nome voluto della nostra img} .
docker build -t todo .

docker images - >  You will get a list of all local Docker images with the tags specified


3) Lanciare il comando o aprire docker dekstop e lanciare eseguire l'img da li

 docker run -d --restart=always -p 8080:{indicare il numero che abbiamo scritto in expose nel dockerfile} todo:tag_name 

If you didn't specify tag_name it will automatically run an image with the 'latest' tag.

Instead of image_name, you can also specify an image ID (no tag_name).


COMANDI UTILI DOCKER (si puo fare tutto da docker dekstop)

docker images - >  You will get a list of all local Docker images with the tags specified.

docker ps - > ci vengono mostrati tutti i contenitori attualmente in esecuzione.

docker ps -a -> avremo una lista di tutti i container presenti, indipendentemente dal loro stato.
