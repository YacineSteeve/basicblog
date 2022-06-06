from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogPostListView.as_view(), name='blog-posts-list'),
    path('blogs/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers-list'),
    path('bloggers/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
