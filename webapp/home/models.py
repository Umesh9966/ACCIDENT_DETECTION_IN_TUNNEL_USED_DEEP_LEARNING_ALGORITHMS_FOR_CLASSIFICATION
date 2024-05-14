from django.db import models
import os


class Register(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)    
    age=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)

class Ccrack(models.Model):
    image = models.ImageField(upload_to="home/static/save")

    def filename(self):
        return os.path.basename(self.image.name)