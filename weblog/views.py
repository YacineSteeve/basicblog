from django.template.context_processors import csrf
from django.views import generic, View
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import BlogPost, Blogger, Comment, Answer, Category
from .forms import CommentForm, AnswerForm, BloggerForm, UserCreateForm


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'key': 'value',
    }
    return render(request, 'index.html', context=context)


# --------- Registration View ---------- #


def account_create(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        blogger_form = BloggerForm(request.POST)

        if user_form.is_valid() and blogger_form.is_valid():
            new_user = user_form.save()
            if request.POST.get('blogger_creation_accepted') == 'on':
                new_blogger = blogger_form.save(commit=False)
                new_blogger.user = new_user

                if request.FILES:
                    new_blogger.avatar = request.FILES.get('avatar')

                new_blogger.save()

            return HttpResponseRedirect(reverse('login'))

    else:
        user_form = UserCreateForm()
        blogger_form = BloggerForm()

    context = {
        'user_form': user_form,
        'blogger_form': blogger_form
    }

    context.update(csrf(request))

    return render(request, 'sign-up_form.html', context)


# ------------ List Views -------------- #


class BlogPostListView(generic.ListView):
    model = BlogPost
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bloggers'] = [blogger.user for blogger in Blogger.objects.all()]
        return context


class BloggerListView(generic.ListView):
    model = Blogger
    paginate_by = 20


# ------------ Detail Views -------------- #


class BlogPostDetailView(generic.DetailView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['answer_form'] = AnswerForm()

        return context


class BloggerDetailView(generic.DetailView):
    model = Blogger


# ------------ Create Views -------------- #


class BlogPostCreate(generic.CreateView):
    model = BlogPost


class CommentCreate(View):
    model = Comment

    def post(self, request, *args, **kwargs):
        Comment(
            blog_post_answered=BlogPost.objects.get(id=self.kwargs['pk']),
            author=User.objects.get(id=self.kwargs['user_id']),
            content=request.POST['content']
        ).save()
        return HttpResponseRedirect(reverse('blog-post-detail', args=[self.kwargs['pk']]))


class AnswerCreate(View):
    model = Answer

    def post(self, request, *args, **kwargs):
        Answer(
            comment_answered=Comment.objects.get(id=self.kwargs['comment_id']),
            author=User.objects.get(id=self.kwargs['user_id']),
            content=request.POST['content']
        ).save()
        return HttpResponseRedirect(reverse('blog-post-detail', args=[self.kwargs['pk']]))


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
