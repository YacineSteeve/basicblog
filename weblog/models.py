from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from collections import OrderedDict
import os
import datetime


def upload_to_user_directory(instance, filename) -> str:
    new_filename = f'{instance.user.username}.{filename[-3:]}'
    return os.path.join(instance.user.username, 'avatar', new_filename)


def convert_timedelta_to_dict(delta: datetime.timedelta) -> dict:
    seconds = delta.seconds % 60
    minutes = ((delta.seconds - seconds) // 60) % 60
    hours = ((delta.seconds - minutes * 60) // 3600) % 86400
    days = delta.days % 7
    weeks = ((delta.days - days) // 7) % 4
    months = ((delta.days - weeks * 7) // 30) % 12
    years = (delta.days - months * 30) // 365

    parsed_delta = OrderedDict({
        'seconds': seconds,
        'minutes': minutes,
        'hours': hours,
        'days': days,
        'weeks': weeks,
        'months': months,
        'years': years
    })

    return parsed_delta


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

    def get_blog_post_age(self) -> str:
        delta = convert_timedelta_to_dict(timezone.now() - self.post_date)
        for time, value in list(delta.items())[:0:-1]:
            if value != 0:
                return f'{value} {time} ago' if value >= 2 else f'{value} {time[:-1]} ago'
        return 'now'

    def get_comments_number(self) -> int:
        comments = self.comment_set.all()
        total = len(comments)
        for comment in comments:
            total += len(comment.answer_set.all())

        return total

    def get_absolute_url(self) -> str:
        return reverse('blog-post-detail', args=[self.id])

    def __str__(self):
        return self.title


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to=upload_to_user_directory, blank=True)
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
    comment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-comment_date', 'author']
        get_latest_by = '-comment_date'

    def get_comment_age(self) -> datetime.timedelta:
        return timezone.now() - self.comment_date

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

    def get_answer_age(self) -> datetime.timedelta:
        return timezone.now() - self.answer_date

    def __str__(self):
        return f'{self.content[:75]}...'


class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name.capitalize()
