from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save(update_fields=["password"])