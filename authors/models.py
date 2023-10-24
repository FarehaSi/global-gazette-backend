from django.db import models
from authentication.models import CustomUser

class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="author")
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

# Signal to automatically create an Author instance when a CustomUser is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_author(sender, instance, **kwargs):
    instance.author.save()
