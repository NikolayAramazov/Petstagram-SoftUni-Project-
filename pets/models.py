from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Pets(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    pet_img = models.ImageField(upload_to='pet_images/')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='pets',null=True)



    def __str__(self):
        return self.name