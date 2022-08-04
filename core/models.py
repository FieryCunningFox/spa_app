from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Article(models.Model):
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

