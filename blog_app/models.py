from django.db import models
from django.utils import timezone
# User: in built django feature that we use on author attribute 
from django.contrib.auth.models import User
from django.urls import reverse

# Los modelos en Django son representaciones de las tablas de la base de datos que definen la estructura 
# y los tipos de datos de los datos que se almacenan y gestionan en la aplicación.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    # si el User se borra, el author se borra
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    # Function que encuntra la url de un post especifico
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
  

