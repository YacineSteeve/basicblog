# Generated by Django 4.0.4 on 2022-06-05 22:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0005_comment_blog_post_answered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 0, 6, 58, 204509)),
        ),
    ]
