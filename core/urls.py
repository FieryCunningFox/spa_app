from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from rest_framework.routers import DefaultRouter

from .views import SignUpView, FeedBackView, SearchView, TagDetailView, TagView, ArticleViewSet, AsideView, ProfileView, CommentView


router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('search/', SearchView.as_view(), name='search'),
    path('tags/', TagView.as_view(), name='tags'),
    path('tags/<slug:tag_slug>', TagDetailView.as_view(), name='tag'),
    path('aside', AsideView.as_view(), name='aside'),
    path('comments/', CommentView.as_view(), name='comments'),
    path('comments/<slug:article_slug>', CommentView.as_view(), name='comment'),
    path('', include(router.urls))
]