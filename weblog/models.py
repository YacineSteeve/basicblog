from django.db import models
from django.urls import reverse
import datetime


class BlogPost(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField('Category', blank=True)
    text_content = models.TextField(max_length=1500, unique=True)
    post_date = models.DateTimeField()

    class Meta:
        ordering = ['-post_date', 'author', 'title']
        get_latest_by = '-post_date'

    def get_blog_post_age(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.post_date

    def get_absolute_url(self):
        return reverse('blog-post-detail', args=['-'.join(self.title)])

    def __str__(self):
        return self.title


class Blogger(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    pseudo = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(max_length=350, upload_to=f'{pseudo}/avatar', blank=True)
    GENDERS = [
        (None, ''),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=4, choices=GENDERS, blank=True)
    date_of_birth = models.DateField()
    join_date = models.DateField()

    class Meta:
        ordering = ['-join_date', 'pseudo']

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[self.pseudo])

    def __str__(self):
        return self.pseudo


class Comment(models.Model):
    author = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=300)
    answers = models.ManyToManyField('self', symmetrical=False, blank=True)
    comment_date = models.DateTimeField()

    class Meta:
        ordering = ['-comment_date', 'author']
        get_latest_by = '-comment_date'

    def get_comment_age(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.comment_date

    def __str__(self):
        return self.content[:50]


class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.capitalize()
