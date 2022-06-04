from django.contrib import admin
from .models import Blogger, BlogPost, Comment, Category


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    pass


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
