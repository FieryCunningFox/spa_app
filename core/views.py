from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import login, authenticate

from .models import Article
from .forms import SignUpForm, SignInForm


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
        
        
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        context = {
            "form": form,
        }
        return render(request, 'core/signup.html', context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            "form": form,
        }
        return render(request, 'core/signup.html', context)
    

class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        context = {
            "form": form,
        }
        return render(request, 'core/signin.html', context)

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            "form": form,
        }
        return render(request, 'core/signin.html', context)