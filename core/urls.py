from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings

from .views import MainView, ArticleDetailView, SignUpView, SignInView, FeedBackView, SuccessView, SearchView, TagView


urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('article/<str:slug>', ArticleDetailView.as_view(), name='article'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('contact/success', SuccessView.as_view(), name='success'),
    path('search/', SearchView.as_view(), name='search'),
    path('tag/<slug:slug>', TagView.as_view(), name='tag'),
]