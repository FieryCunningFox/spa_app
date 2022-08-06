from django.urls import path
from .views import MainView, ArticleDetailView


urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('article/<str:slug>', ArticleDetailView.as_view(), name='article'),
]