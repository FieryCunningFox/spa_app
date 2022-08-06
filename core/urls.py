from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings

from .views import MainView, ArticleDetailView, SignUpView, SignInView


urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('article/<str:slug>', ArticleDetailView.as_view(), name='article'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
]