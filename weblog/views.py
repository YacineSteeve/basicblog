from django.template.context_processors import csrf
from django.views import generic, View
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import BlogPost, Blogger, Comment, Answer
from .forms import BloggerForm, CommentForm, AnswerForm, CategoryForm, UserCreateForm, ContactForm


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'key': 'value',
    }
    return render(request, 'index.html', context)


# --------- Registration View ---------- #


def account_create(request: HttpRequest) -> HttpResponse:
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


def account_update(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=pk)

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


def account_delete(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=pk)
    if request.method == 'POST' and user == request.user:
        logout(request)
        user.delete()
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'confirm_delete.html', {'object': user})


def contact_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            send_mail(
                subject=contact_form.cleaned_data['subject'],
                message=contact_form.cleaned_data['message'],
                from_email=contact_form.cleaned_data['sender_email'],
                recipient_list=[]
            )
    else:
        if request.user.is_authenticated:
            contact_form = ContactForm(sender_email=request.user.email)
        else:
            contact_form = ContactForm()

    return render(request, 'base.html', {'contact_form': contact_form})


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
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['answer_form'] = AnswerForm()
        return context


class BloggerDetailView(generic.DetailView):
    model = Blogger


# ------------ Create Views -------------- #


class BlogPostCreate(generic.CreateView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = CategoryForm()
        return context


class BloggerCreate(generic.CreateView):
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


# ------------ Update Views -------------- #


class BlogPostUpdate(generic.UpdateView):
    model = BlogPost


# ------------ Delete Views -------------- #


class BloggerDelete(generic.DeleteView):
    model = Blogger
    template_name = 'confirm_delete.html'
    success_url = '/weblog/'


class BlogPostDelete(generic.DeleteView):
    model = BlogPost
