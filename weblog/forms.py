from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.core.exceptions import ValidationError
from .models import Blogger, Comment, Answer


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['blog_post_answered', 'author', 'content', 'comment_date']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['comment_answered', 'author', 'content', 'answer_date']


class BloggerForm(ModelForm):
    class Meta:
        model = Blogger
        exclude = ['user']


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             label='Email',
                             error_messages={'exists': 'This email is already used.'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']
