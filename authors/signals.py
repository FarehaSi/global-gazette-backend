from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import CustomUser
from .models import Author

@receiver(post_save, sender=CustomUser)
def create_author(sender, instance=None, created=False, **kwargs):
    if created:
        Author.objects.create(user=instance)
