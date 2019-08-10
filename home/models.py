from django.db import models

# Create your models here.
class Test(models.Model): 
    Img_test = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50) 
