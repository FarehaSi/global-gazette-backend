from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = CloudinaryField(
        'image', folder='profile_pics/', blank=True
    )
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following', blank=True
    )
    full_name = models.CharField(max_length=255, blank=True)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save(update_fields=["password"])
