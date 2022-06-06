from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import os
import datetime


def upload_to_user_directory(instance, filename) -> str:
    new_filename = f'{instance.user.username}.{filename[-3:]}'
    return os.path.join(instance.user.username, 'avatar', new_filename)


class BlogPost(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField('Category', blank=True)
    text_content = models.TextField(max_length=1500, unique=True)
    post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-post_date', 'author', 'title']
        get_latest_by = '-post_date'

    def get_blog_post_age(self) -> datetime.timedelta:
        return timezone.now() - self.post_date

    def get_absolute_url(self) -> str:
        return reverse('blog-post-detail', args=['-'.join(self.title)])

    def __str__(self):
        return self.title


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to=upload_to_user_directory, blank=True)
    GENDERS = [
        (None, ''),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=4, choices=GENDERS, blank=True)
    date_of_birth = models.DateField()

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
    answers = models.ManyToManyField('self', symmetrical=False, blank=True)
    comment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-comment_date', 'author']
        get_latest_by = '-comment_date'

    def get_comment_age(self) -> datetime.timedelta:
        return timezone.now() - self.comment_date

    def __str__(self):
        return f'{self.content[:50]}...'


class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name.capitalize()
