from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create/', views.account_create, name='create-account'),
    path('blogs/', views.BlogPostListView.as_view(), name='blog-posts-list'),
    path('blogs/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('blogs/<int:pk>/<int:user_id>/comments/create/', views.CommentCreate.as_view(), name='comment-create'),
    path('blogs/<int:pk>/<int:user_id>/<int:comment_id>/answers/create/', views.AnswerCreate.as_view(), name='answer-create'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers-list'),
    path('bloggers/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
