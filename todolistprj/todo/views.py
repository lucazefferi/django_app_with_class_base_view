from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin #importa il metodo per gestire quali pagine e cosa possono fare gli utenti se non sono loggati


# Create your views here.
def index(request):
     return render(request, "todo/index.html")

#Function views
#def task_list(request):
#@login_required
#def task_list(request):
    #tasks = Task.objects.filter(user=request.user)
    #count = tasks.filter(complete=False).count()
    #context = {'tasks': tasks, 'count': count}
    #return render(request, 'todo/task_list.html', context)


#LoginRequiredMixin passando questo param l'utente per performare questa azione deve essere loggato
#nella view invece uso {% if request.user.is_authenticated %} che ci permette di nascondere elementi 
#che non vogliamo mostrare a persone non autenticate 
#SPIEGAZIONE METODO TaskList
#class TaskList(LoginRequiredMixin, ListView): Questa riga definisce una nuova vista basata su classi. LoginRequiredMixin è un mixin che assicura che solo gli utenti autenticati possano accedere a questa vista. ListView è una vista generica in Django per visualizzare una lista di oggetti.
#model = Task Questa riga indica che la vista si basa sul modello Task. Django utilizzerà questo modello per creare una lista di oggetti Task.
#context_object_name = 'tasks' Questa riga indica che gli oggetti recuperati dal modello Task saranno disponibili nel template con il nome tasks.
#def get_context_data(self, **kwargs): Questo è un metodo della superclasse ListView che Django chiama per ottenere il contesto del template. Il contesto è un dizionario che mappa i nomi delle variabili ai loro valori.
#context = super().get_context_data(**kwargs) Questa riga chiama il metodo get_context_data della superclasse (in questo caso, ListView) per ottenere il contesto di base.
#context['tasks'] = context['tasks'].filter(user_id=self.request.user) Questa riga filtra gli oggetti Task nel contesto per includere solo quelli che appartengono all’utente corrente, lo fa verificando user_id se corrisponde alla FK del task 
#context['count'] = context['tasks'].filter(complete=False).count() Questa riga conta quanti task non sono completati e aggiunge questo conteggio al contesto con il nome count.
#return context Infine, il metodo restituisce il contesto che sarà utilizzato dal template.
#Class based views
class TaskList(LoginRequiredMixin, ListView):
     model = Task
     context_object_name = 'tasks'

#Il metodo get_context_data viene eseguito automaticamente da Django ogni volta che la vista TaskList
#viene richiesta da un utente. Questo avviene quando un utente visita l’URL associato a questa vista nel tuo file urls.py.
     def get_context_data(self, **kwargs):

          #Quando chiami super().get_context_data(**kwargs), stai ottenendo il contesto standard che ListView fornisce,
          #che include la lista di oggetti  da visualizzare nel template (in questo caso, oggetti di tipo modello Task, salvata sotto la voce -> context_object_name = 'tasks' )
          #in che modo  ListView rende disponibili questo oggetti? dietro le quinte, va a salvare nel dizionario context, in questo caso, sotto la chiave tasks
          #context['tasks'] tutta la lista di oggetti con alla quale fa riferimento in questo caso sta lavorando entità model=Task, come se facesse request.setAttribute("tasks", tasks)
          #infatti poi nella task_list.html accediamo al OBJ task e facciamo un ciclo For

          #noi in questo caso poi abbiamo recuperato il contesto e lo abbiamo filtrato lasciando solo gli OBJ appartenenti allo user che sta effetuando la richiesta e se c'è
          #il paramtro search_input abbiamo ulteriormente filtarato lascindo solo gli OBJ che nel titolo includono la parola cercata
          
          #mi prendo il parametro nella url
          search_input = self.request.GET.get('search-task') or ''
          print(f"parola: {search_input}")

          context = super().get_context_data(**kwargs)
          #il modello task ha il campo user_id ecco perché uso quello 
          context['tasks'] = context['tasks'].filter(user_id=self.request.user)
          context['count'] = context['tasks'].filter(complete=False).count()
          
          if search_input:
               #il modello task ha il campo title ecco perché uso quello dicendo filtra se la parola cercata è inclusa nel attr title del mio OBJ
               context['tasks'] = context['tasks'].filter(title__icontains=search_input)
               #context['tasks'] = context['tasks'].filter(title__startwith=search_input)
               context['search_input'] = search_input
     
          return context
          
    
#Function based views
#def task_detail(request, task_id):
    #task = Task.objects.get(id=task_id)
    #return render(request, 'todo/task_detail.html', {'task': task})

#Class based views
class TaskDetail(LoginRequiredMixin, DetailView):
     model = Task
     context_object_name = 'task'
     #se volessi cambiare il nome del template potrei fare cosi, ovviamente dovrei chiamare il file con lo stesso nome
     #template_name = 'todo/task_detail_upt.html'

#Class based views
class TaskCreate(LoginRequiredMixin, CreateView):
     model = Task
     #ci permette di scegliere quali campi saranno visibili
     fields = ["title", "description", "complete"]
     #ci permette di rendere visibili tutti i campi de modello
     #fields = "__all__" 

     #if we are using success_url we have to use reverse_lazy().
     #if we are reversing inside a function we can use reverse().
     #serve per configurare dove mandarci una volta salvato il nuovo task
     success_url = reverse_lazy('todo:task_list')

     #metodo eseguito quando c'è un errore
     def form_invalid(self, form):
          return super(CreateView, self).form_valid(form)
         
     def form_valid(self, form):
          #è come se prendessi il campo user_id del form e gli assegnassi l'utente corrente
          form.instance.user_id = self.request.user
          return super(CreateView, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
     model = Task
     fields = ["title", "description", "complete"]
     context_object_name = 'task'
     success_url = reverse_lazy('todo:task_list')

#in questo modo mostro un form con un tasto per confermare la delete 
class TaskDelete(LoginRequiredMixin, DeleteView):
     model = Task
     context_object_name = 'task'
     success_url = reverse_lazy('todo:task_list')

#se avessi voluto eliminare direttamente senza mostrare la view e senza usare le class based view posso utilizzare le function view 
#def task_delete(request, task_id):
    #if request.method == 'POST':
        #task = Task.objects.get(pk=task_id)
        #task.delete()
        #return redirect('todo:task_list')
     #else
     #return render(request, "todo/task_confirm_delete.html")    


#questo è il path per far loggare l'utente, il path per il logout non serve, 
#ma bisona solo specificare il path nella urls.py ed importare LogoutView
#IDCOMMENTO1
#!!IMPORTANTE QUESO METODO COME VEDI NON FA UN CONTROLLO SUL TIPO DI RICHIESTA, MA AUTAMATICAMENTE UTILIZZA IL CONTENUTO DELLA CLASSE A SECONDA DELLA RICHIESTA CHE GLI ARRIVA
#SE GLI ARRIVA UN GET ESEGUIRA I METODI E UTILIZZERA LE VARIABILI ASSOCIATI ALLA GET COME PER ESEMPIO template_name CHE SERVE ALLA GET PER SAPERE QUALE PAGINA MOSTRARE,
#SE GLI ARRIVA UNA POST ESEGUIRA I METODI E UTILIZZERA LE VARIABILI ASSOCIATI ALLA POST COME PER ESEMPIO get_success_url CHE SERVE ALLA POST PER SAPERE DOVE MANDARE L'UTENTE UNA VOLTA CHE LA CHIAMATA è ANDATA A BUON FINE,

class CustomLoginView(LoginView):
     template_name = 'todo/login.html' #serve sempre
     field = "__all__"
     redirect_authenticated_user = False

     #metodo eseguito quando l'utente si è loggato
     def get_success_url(self):
          return reverse_lazy('todo:task_list')

#IDCOMMENTO2    
#QUI HO FATTO UN OVERIDE DEI METODI GET E POST, IL METODO GET VIENE CHIAMATO QUANDO GLI ARRIVA UNA RICHIESTA GET, E IL METODO POST QUANDO GLI ARRIVA 
#UNA RICHIESTA POST.
#ES: se non abbiamo SOVRASCRITTO il metodo GET LUI NON ESEGUIRA NESSUNA LOGICA PERSONALIZZATA MA UTILIZZERA DIRETTAMENTE IL
#METODO DELLA SUA SUPERCLASSE ALTRIMENTI ESEGUIRA LA NOSTRA LOGICA E POI IN ENTRAMBI I CASI SIA CHE ABBIAMO FATTO OVERIDE CHE NON, ANDRA AD USARE LA VAR template_name PER SAPERE QUALE PAGINA MOSTRARE

#ES: se non abbiamo SOVRASCRITTO il metodo POST LUI NON ESEGUIRA NESSUNA LOGICA PERSONALIZZATA MA UTILIZZERA IL METODO DELLA
#SUA SUPERCLASSE ALTRIMENTI ESEGUIRA LA NOSTRA LOGICA E POI IN ENTRAMBI I CASI SIA CHE ABBIAMO FATTO OVERIDE CHE NON, ANDRA AD USARE LA FUNZIONE get_success_url

#class CustomLoginView(LoginView):
    #template_name = 'todo/login.html'
    #fields = "__all__"
    #redirect_authenticated_user = False

    #def get(self, request, *args, **kwargs):
        # Logica personalizzata per le richieste GET
        #return super().get(request, *args, **kwargs)

    #def post(self, request, *args, **kwargs):
        # Logica personalizzata per le richieste POST
        #return super().post(request, *args, **kwargs)

    #def get_success_url(self):
        #return reverse_lazy('todo:task_list')


class CustomRegisterView(FormView):
     template_name = 'todo/register.html' #serve sempre
     form_class = UserCreationForm
     redirect_authenticated_user = True
     success_url = reverse_lazy('todo:task_list')
    
     #metodo eseguito quando l'utente preme invio del form e il form è valido,
     #a differenza di get_success_url, form_valid o form_ivalid ci permettono di manipolare il form infatti viene passato il parametro form
     #una volta fatto chiama automaticamente l'attr success_url che fa la stessa cosa di get_success_url
     def form_valid(self, form):
          user = form.save()
          if user is not None:
               login(self.request, user)
          else:
               return render(self.request, 'todo/register.html', {'form': form}) #gli passo l'obj form che poi viene renderizzato con {{form}} e un obj ereditato da FormView ma che per esempio possiede CreateView
                                                                                 
          return super(CustomRegisterView, self).form_valid(form)
     
