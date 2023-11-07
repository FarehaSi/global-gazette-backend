from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    thumbnail = CloudinaryField('image', null=True, blank=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    # thumbnail = models.ImageField(upload_to='article_thumbnails/')
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Reaction(models.Model):
    REACTION_TYPE_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="article_reactions", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('Comment', related_name="comment_reactions", on_delete=models.CASCADE, null=True, blank=True)
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.article:
            if self.reaction_type == 'like':
                self.article.likes_count += 1
            elif self.reaction_type == 'dislike':
                self.article.dislikes_count += 1
            self.article.save()
        elif self.comment:
            if self.reaction_type == 'like':
                self.comment.likes_count += 1
            elif self.reaction_type == 'dislike':
                self.comment.dislikes_count += 1
            self.comment.save()


    def delete(self, *args, **kwargs):
        if self.article:
            if self.reaction_type == 'like' and self.article.likes_count > 0:
                self.article.likes_count -= 1
            elif self.reaction_type == 'dislike' and self.article.dislikes_count > 0:
                self.article.dislikes_count -= 1
            self.article.save()
        elif self.comment:
            if self.reaction_type == 'like' and self.comment.likes_count > 0:
                self.comment.likes_count -= 1
            elif self.reaction_type == 'dislike' and self.comment.dislikes_count > 0:
                self.comment.dislikes_count -= 1
            self.comment.save()
        super().delete(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.article.comments_count += 1
        self.article.save()
    
    def delete(self, *args, **kwargs):
        self.article.comments_count -= 1
        self.article.save()
        super().delete(*args, **kwargs)
