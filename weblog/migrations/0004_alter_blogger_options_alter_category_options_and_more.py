# Generated by Django 4.0.4 on 2022-06-04 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0003_alter_blogger_options_remove_blogger_pseudo_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogger',
            options={'ordering': ['user']},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'categories'},
        ),
        migrations.RemoveField(
            model_name='blogger',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='blogger',
            name='join_date',
        ),
        migrations.RemoveField(
            model_name='blogger',
            name='last_name',
        ),
    ]
