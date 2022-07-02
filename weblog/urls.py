from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.recent_posts, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create/', views.account_create, name='account-create'),
    path('accounts/<int:pk>/update/', views.account_update, name='account-update'),
    path('accounts/<int:pk>/delete/', views.account_delete, name='account-delete'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers-list'),
    path('bloggers/create/', views.BloggerCreate.as_view(), name='blogger-create'),
    path('bloggers/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('bloggers/<int:pk>/delete/', views.BloggerDelete.as_view(), name='blogger-delete'),
    path('blogs/', views.BlogPostListView.as_view(), name='blog-posts-list'),
    path('blogs/create/', views.BlogPostCreate.as_view(), name='blog-post-create'),
    path('blogs/search/<str:category>/', views.blog_posts_of_given_category, name='category-blog-posts'),
    path('blogs/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('blogs/<int:pk>/delete/', views.BlogPostDelete.as_view(), name='blog-post-delete'),
    path('blogs/<int:pk>/<int:user_id>/comments/create/', views.CommentCreate.as_view(), name='comment-create'),
    path('blogs/<int:pk>/<int:user_id>/<int:comment_id>/answers/create/', views.AnswerCreate.as_view(), name='answer-create'),
    path('search/', views.search, name='search-results'),
    path('contact/', views.contact_view, name='message-send')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
