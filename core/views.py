from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.core.paginator import Paginator
from taggit.models import Tag
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import filters

from .models import Article, Comment
from .forms import SignUpForm, SignInForm, FeedBackForm, CommentForm
from .serializers import ArticleSerializer, TagSerializer, ContactSerializer, RegistrationSerializer, UserSerializer, CommentSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class ArticleViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination
        
        
class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User successfully registered",
        })
    
    
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request, *args,  **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })
        
    
class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer
    
    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'From {name} | {subject}', message, from_email, ['svetl.rudnewa2014@gmail.com'])
            return Response({"success": "Sent"})


class SearchView(View):
    pass
    # def get(self, request, *args, **kwargs):
    #     if query := self.request.GET.get('q'):
    #         results = Article.objects.filter(Q(h1__icontains=query) | Q(content__icontains=query) | Q(title__icontains=query))
    #     else:
    #         results = ""
    #     paginator = Paginator(results, 6)
    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     context = {
    #         "title": "Search", 
    #         "results": page_obj,
    #         "count": paginator.count,
    #     }
    #     return render(request, 'core/search.html', context)
    
    
class TagDetailView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Article.objects.filter(tags=tag)
    

class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    
    
class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        article_slug = self.kwargs['article_slug'].lower()
        article = Article.objects.get(slug=article_slug)
        return Comment.objects.filter(article=article)


class AsideView(generics.ListAPIView):
    queryset = Article.objects.all().order_by('-id')[:5]
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]