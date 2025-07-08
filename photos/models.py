from django.contrib.auth.models import User
from django.db import models

from pets.models import Pets


# Create your models here.
class Photo(models.Model):
     photo = models.ImageField()
     description = models.TextField()
     location = models.CharField(max_length=100)
     tagged_pet = models.ManyToManyField(Pets)
     owner = models.ForeignKey(User, related_name='photos', on_delete=models.CASCADE)

class Comment(models.Model):
    photo = models.ForeignKey(Photo, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented {self.content}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'photo')  # Prevent multiple likes from the same user

    def __str__(self):
        return f"{self.user.username} likes Photo #{self.photo.id}"