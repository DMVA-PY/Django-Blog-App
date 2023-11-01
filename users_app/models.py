from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Los modelos en Django son representaciones de las tablas de la base de datos que definen la estructura 
# y los tipos de datos de los datos que se almacenan y gestionan en la aplicación.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)