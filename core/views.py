from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import Http404

from .models import Article


class MainView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        context = {
            "articles": articles,
        }
        return render(request, 'core/home.html', context)
    
    
class ArticleDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        try:
            article = get_object_or_404(Article, url=slug)
            context = {
                "article": article,
            }
            return render(request, 'core/article_detail.html', context)
        except Article.DoesNotExist:
            return Http404