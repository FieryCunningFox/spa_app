from django.shortcuts import render
from django.views import View

from .models import Article


class MainView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        context = {
            "articles": articles,
        }
        return render(request, 'core/home.html', context)
    
    
    