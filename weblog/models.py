from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import os


def upload_to_user_directory(instance, filename) -> str:
    new_filename = f'{instance.user.username}.{filename[-3:]}'
    return os.path.join(instance.user.username, 'avatar', new_filename)


class BlogPost(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField('Category', blank=True)
    content = models.TextField(max_length=1500, unique=True)
    post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-post_date', 'author', 'title']
        get_latest_by = '-post_date'

    def get_categories(self) -> list:
        return [category for category in self.categories.all()]

    def get_comments_number(self) -> int:
        comments = [comment for comment in self.comment_set.all() if not comment.author.is_superuser]
        total = len(comments)
        for comment in comments:
            answers = [answer for answer in comment.answer_set.all() if not answer.author.is_superuser]
            total += len(answers)

        return total

    def get_absolute_url(self) -> str:
        return reverse('blog-post-detail', args=[self.id])

    def __str__(self):
        return self.title


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, editable=False)
    avatar = models.ImageField(upload_to=upload_to_user_directory, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['user']

    def get_absolute_url(self) -> str:
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    blog_post_answered = models.ForeignKey('BlogPost', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=300)
    comment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-comment_date', 'author']
        get_latest_by = '-comment_date'

    def __str__(self):
        return f'{self.content[:75]}...'


class Answer(models.Model):
    comment_answered = models.ForeignKey('Comment', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=300)
    answer_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-answer_date', 'author']
        get_latest_by = '-answer_date'

    def __str__(self):
        return f'{self.content[:75]}...'


class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name.capitalize()
