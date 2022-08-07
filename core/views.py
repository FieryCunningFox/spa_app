from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.core.paginator import Paginator
from taggit.models import Tag

from .models import Article, Comment
from .forms import SignUpForm, SignInForm, FeedBackForm, CommentForm


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
            common_tags = Article.tag.most_common()
            last_articles = Article.objects.all().order_by('-id')[:5]
            context = {
                "article": article,
                "common_tags": common_tags,
                "last_articles": last_articles
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
            results = Article.objects.filter(Q(h1__icontains=query) | Q(content__icontains=query) | Q(title__icontains=query))
        else:
            results = ""
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "title": "Search", 
            "results": page_obj,
            "count": paginator.count,
        }
        return render(request, 'core/search.html', context)
    
    
class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        articles = Article.objects.filter(tag=tag).order_by('created_at')
        common_tags = Article.tag.most_common()
        context = {
            "title": f"#{tag}",
            "articles": articles,
            "common_tags": common_tags
        }
        return render(request, 'core/tag.html', context)
    
    
class CommentView(View):
    def get(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, url=slug)
        common_tags = Article.tag.most_common()
        last_articles = Article.objects.all().order_by('-id')[:5]
        comment_form = CommentForm()
        context = {
            "article": article,
            "common_tags": common_tags,
            "last_articles": last_articles,
            "comment_form": comment_form,
        }
        return render(request, 'core/article_detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            article = get_object_or_404(Article, url=slug)
            comment = Comment.objects.create(post=article, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        context = {
            "comment_form": comment_form,
        }
        return render(request, 'core/article_detail.html', context)

