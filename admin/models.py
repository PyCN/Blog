from django.db import models


# Create your models here.

class Images(models.Model):
    image = models.ImageField(upload_to='%Y/%m', max_length=100)