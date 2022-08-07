from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q

from .models import Article
from .forms import SignUpForm, SignInForm, FeedBackForm


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
    
    
class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        context = {
            "form": form,
            "title": "Write message"
        }
        return render(request, 'core/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'From {name} | {subject}', message, from_email, ['svetl.rudnewa2014@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header')
            return HttpResponseRedirect('success')
        context = {
            'form': form
            }
        return render(request, 'core/contact.html', context)


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "title": "Thank you for your message"
        }
        return render(request, 'core/success.html', context)


class SearchView(View):
    def get(self, request, *args, **kwargs):
        if query := self.request.GET.get('q'):
            results = Article.objects.filter(Q(h1__icontains=query) | Q(content__icontains=query))

        else:
            results = ""
        context = {"title": "Search", "results": results, "count": len(results)}
        return render(request, 'core/search.html', context)