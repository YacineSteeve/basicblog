from django.views import generic
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import BlogPost, Blogger


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'key': 'value',
    }
    return render(request, 'index.html', context=context)


class BlogPostListView(generic.ListView):
    model = BlogPost
    paginate_by = 5


class BloggerListView(generic.ListView):
    model = Blogger
    paginate_by = 20


class BlogPostDetailView(generic.DetailView):
    model = BlogPost


class BloggerDetailView(generic.DetailView):
    model = Blogger
