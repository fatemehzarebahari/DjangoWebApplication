# Generated by Django 4.2.9 on 2024-01-28 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_like_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='music',
            name='likes',
        ),
    ]