# Generated by Django 4.0.4 on 2022-06-20 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0013_remove_blogger_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
