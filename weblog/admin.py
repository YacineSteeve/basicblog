from django.contrib import admin
from .models import Blogger, BlogPost, Comment, Answer, Category


admin.site.register(Category)
admin.site.register(Answer)


class BlogPostInline(admin.TabularInline):
    model = BlogPost
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    inlines = [
        BlogPostInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]
