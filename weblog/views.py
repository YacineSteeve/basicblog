from django.conf import settings
from django.template.context_processors import csrf
from django.views import generic, View
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables
from .models import BlogPost, Blogger, Comment, Answer, Category
from .forms import BlogPostForm, BloggerForm, CommentForm, AnswerForm, \
    CategoryForm, UserCreateForm, SearchForm, ContactForm


def recent_posts(request: HttpRequest) -> HttpResponse:
    blogposts = BlogPost.objects.all()
    sorted_posts = sorted(blogposts, key=lambda blogpost: blogpost.post_date, reverse=True)
    return render(request, 'index.html', {'recent_posts': sorted_posts})


def blog_posts_of_given_category(request: HttpRequest, category: str) -> HttpResponse:
    blogposts = BlogPost.objects.filter(categories__name=category)
    return render(request, 'category_blogposts.html', {'category': category,
                                                       'blogposts_of_category': blogposts})


def search(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['query']
            if search_query != '':
                matching_categories = []
                matching_posts = []
                matching_bloggers = []

                for word in search_query.split(' '):
                    matching_categories += Category.objects.filter(name__icontains=word)
                    matching_posts += BlogPost.objects.filter(title__icontains=word)
                    matching_posts += BlogPost.objects.filter(content__icontains=word)
                    matching_bloggers += Blogger.objects.filter(user__username__icontains=word)

                context = {
                    'query': search_query,
                    'matching_categories': matching_categories[:15],
                    'matching_posts': matching_posts[:15],
                    'matching_bloggers': matching_bloggers[:15]
                }

                return render(request, 'search.html', context)

    return HttpResponseRedirect(reverse('index'))


@sensitive_post_parameters('password1', 'password2')
@sensitive_variables('user_form', 'new_user')
def account_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        blogger_form = BloggerForm(request.POST, request.FILES)

        if user_form.is_valid() and blogger_form.is_valid():
            new_user = user_form.save()

            if request.POST['blogger_creation_accepted'] == 'on':
                new_blogger = blogger_form.save(commit=False)
                new_blogger.user = new_user
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


@sensitive_post_parameters('old_password', 'new_password1', 'new_password2')
@sensitive_variables('form2', 'password_form')
@login_required
def account_update(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=pk)

    if user == request.user:
        try:
            blogger = Blogger.objects.get(user=user)
        except Blogger.DoesNotExist:
            is_blogger = False
            current_date_of_birth = ''
        else:
            is_blogger = True
            current_date_of_birth = blogger.date_of_birth

        if request.method == 'POST':
            form1 = BloggerForm(request.POST, request.FILES)
            form2 = PasswordChangeForm(user=user, data=request.POST)

            if is_blogger:
                if form1.is_valid():
                    blogger = Blogger.objects.get(user=user)
                    new_avatar = form1.cleaned_data['avatar']
                    new_date_of_birth = form1.cleaned_data['date_of_birth']

                    if new_avatar:
                        blogger.avatar = new_avatar
                    if new_date_of_birth and str(new_date_of_birth) != str(current_date_of_birth):
                        blogger.date_of_birth = new_date_of_birth

                    blogger.save()

            if form2.is_valid():
                user.set_password(form2.cleaned_data['new_password2'])
                user.save()
                return HttpResponseRedirect(reverse('login'))

            if 'avatar' in request.POST:
                password_form = PasswordChangeForm(user=user)
                blogger_form = form1
            else:
                password_form = form2
                blogger_form = BloggerForm()
        else:
            password_form = PasswordChangeForm(user=user)
            blogger_form = BloggerForm()

        context = {
            'user': user,
            'password_form': password_form,
            'blogger_form': blogger_form,
            'current_date_of_birth': current_date_of_birth,
        }

        context.update(csrf(request))

        return render(request, 'account_update.html', context)
    else:
        return HttpResponseRedirect(reverse('index'))


@login_required
def account_delete(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=pk)

    if user == request.user:
        if request.method == 'POST' and user == request.user:
            logout(request)
            user.delete()
            return HttpResponseRedirect(reverse('index'))

        return render(request, 'confirm_delete.html', {'object': user})
    else:
        return HttpResponseRedirect(reverse('index'))


def contact_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ContactForm(request.POST)
        recipient_list = [person[1] for person in settings.ADMINS]

        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['sender_email'],
                recipient_list=recipient_list
            )

        return render(request, 'contact_done_or_not.html', {'form': form})

    return HttpResponseRedirect(reverse('index'))


class BlogPostListView(generic.ListView):
    model = BlogPost
    paginate_by = 20


class BloggerListView(generic.ListView):
    model = Blogger
    paginate_by = 20


class BlogPostDetailView(generic.DetailView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['answer_form'] = AnswerForm()
        return context


class BloggerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Blogger


class BlogPostCreate(LoginRequiredMixin, generic.CreateView):
    model = BlogPost
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form1 = CategoryForm(request.POST)
        form2 = BlogPostForm(request.POST)

        if form1.is_valid():
            form1.save()
            return render(request, 'blogpost_form.html', {
                'blogpost_form': BlogPostForm(),
                'category_form': form1,
            })

        if form2.is_valid():
            form2.save()
            return HttpResponseRedirect(reverse('blog-posts-list'))

        context = {
            'blogpost_form': form2,
            'category_form': form1,
        }

        return render(request, 'blogpost_form.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogpost_form'] = BlogPostForm()
        context['category_form'] = CategoryForm()
        return context


class BloggerCreate(LoginRequiredMixin, generic.CreateView):
    model = Blogger
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form = BloggerForm(request.POST, request.FILES)
        user = User.objects.get(id=request.user.id)

        if form.is_valid():
            Blogger(
                user=user,
                avatar=form.cleaned_data['avatar'],
                date_of_birth=form.cleaned_data['date_of_birth']
            ).save()
        else:
            return render(request, 'blogger_form.html', {'form': form})

        return HttpResponseRedirect(reverse('account-update', args=[request.user.id]))


class CommentCreate(LoginRequiredMixin, View):
    model = Comment

    def post(self, request, *args, **kwargs):
        Comment(
            blog_post_answered=BlogPost.objects.get(id=self.kwargs['pk']),
            author=User.objects.get(id=self.kwargs['user_id']),
            content=request.POST['content']
        ).save()
        return HttpResponseRedirect(reverse('blog-post-detail', args=[self.kwargs['pk']]))


class AnswerCreate(LoginRequiredMixin, View):
    model = Answer

    def post(self, request, *args, **kwargs):
        Answer(
            comment_answered=Comment.objects.get(id=self.kwargs['comment_id']),
            author=User.objects.get(id=self.kwargs['user_id']),
            content=request.POST['content']
        ).save()
        return HttpResponseRedirect(reverse('blog-post-detail', args=[self.kwargs['pk']]))


class BloggerDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Blogger
    permission_required = 'weblog.can_manage_blogger_data'
    template_name = 'confirm_delete.html'
    success_url = '/weblog/'

    def test_func(self):
        blogger_to_delete = Blogger.objects.get(id=self.kwargs['pk'])
        return self.request.user.blogger and self.request.user.blogger == blogger_to_delete


class BlogPostDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BlogPost
    permission_required = 'weblog.can_manage_blogger_data'
    template_name = 'confirm_delete.html'
    success_url = '/weblog/blogs/'

    def test_func(self):
        blogpost_to_delete = BlogPost.objects.get(id=self.kwargs['pk'])
        return self.request.user.blogger and blogpost_to_delete.author == self.request.user.blogger
