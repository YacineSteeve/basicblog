from django.views import generic
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import BlogPost, Blogger, Comment, Answer, Category


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'key': 'value',
    }
    return render(request, 'index.html', context=context)


# ------------ List Views -------------- #


class BlogPostListView(generic.ListView):
    model = BlogPost
    paginate_by = 10


class BloggerListView(generic.ListView):
    model = Blogger
    paginate_by = 20

# ------------ Detail Views -------------- #


class BlogPostDetailView(generic.DetailView):
    model = BlogPost


class BloggerDetailView(generic.DetailView):
    model = Blogger

# ------------ Create Views -------------- #


class BloggerCreate(generic.CreateView):
    model = Blogger


class BlogPostCreate(generic.CreateView):
    model = BlogPost


class CommentCreate(generic.CreateView):
    model = Comment


class AnswerCreate(generic.CreateView):
    model = Answer


class CategoryCreate(generic.CreateView):
    model = Category

# ------------ Update Views -------------- #


class BloggerUpdate(generic.CreateView):
    model = Blogger


class BlogPostUpdate(generic.CreateView):
    model = BlogPost


class CategoryUpdate(generic.CreateView):
    model = Category

# ------------ Delete Views -------------- #


class BloggerDelete(generic.CreateView):
    model = Blogger


class BlogPostDelete(generic.CreateView):
    model = BlogPost


class CommentDelete(generic.CreateView):
    model = Comment


class AnswerDelete(generic.CreateView):
    model = Answer


class CategoryDelete(generic.CreateView):
    model = Category
