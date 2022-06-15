from django.forms.models import ModelForm
from .models import Comment, Answer


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['blog_post_answered', 'author', 'content', 'comment_date']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['comment_answered', 'author', 'content', 'answer_date']
