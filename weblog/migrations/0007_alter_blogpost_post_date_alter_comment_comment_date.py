# Generated by Django 4.0.4 on 2022-06-05 22:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0006_alter_blogpost_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 0, 8, 3, 652145)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 0, 8, 3, 653760)),
        ),
    ]
