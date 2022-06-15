from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from .models import BlogPost, Blogger, Comment, Answer, Category
from .forms import CommentForm, AnswerForm


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

    def get_context_data(self, **kwargs):
        comment_form = CommentForm(initial={
            'blog_post_answered': self.object,
            'author': self.object.author,
        })
        answer_form = AnswerForm()

        context = super().get_context_data(**kwargs)
        context['comment_form'] = comment_form
        context['answer_form'] = answer_form

        return context


class BloggerDetailView(generic.DetailView):
    model = Blogger

# ------------ Create Views -------------- #


class BloggerCreate(generic.CreateView):
    model = Blogger


class BlogPostCreate(generic.CreateView):
    model = BlogPost


class CommentCreate(generic.CreateView):
    model = Comment
    fields = ['blog_post_answered', 'author', 'content', 'comment_date']
    success_url = reverse_lazy('blog-post-detail')


class AnswerCreate(generic.CreateView):
    model = Answer


class CategoryCreate(generic.CreateView):
    model = Category

# ------------ Update Views -------------- #


class BloggerUpdate(generic.UpdateView):
    model = Blogger


class BlogPostUpdate(generic.UpdateView):
    model = BlogPost


class CategoryUpdate(generic.UpdateView):
    model = Category

# ------------ Delete Views -------------- #


class BloggerDelete(generic.DeleteView):
    model = Blogger


class BlogPostDelete(generic.DeleteView):
    model = BlogPost


class CommentDelete(generic.DeleteView):
    model = Comment


class AnswerDelete(generic.DeleteView):
    model = Answer


class CategoryDelete(generic.DeleteView):
    model = Category
