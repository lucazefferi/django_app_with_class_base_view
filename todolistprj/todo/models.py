from django.db import models
from django.contrib.auth.models import User #sto importando il modello user che djano ci mette a disposizione, lui crea una tabella User
# Create your models here.

class Task(models.Model):
    #In sintesi, null=True riguarda il modo in cui i dati vengono salvati nel database, 
    #mentre blank=True riguarda la validazione dei dati nei form. 
    #Entrambi impostati a True significa che sia nel database che nei form, user_id può essere omesso.
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True) #aggiunge direttamente la data di quando è creato 

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete'] #i task completati saranno sul fondo
