from django.db import models
from django.contrib.auth.models import User

from photos.models import Photo


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(default='profile_images/user.png', upload_to='profile_images/')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)



    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_messages')
    content = models.TextField()
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.content[:20]}"