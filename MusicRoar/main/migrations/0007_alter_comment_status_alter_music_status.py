# Generated by Django 4.2.9 on 2024-01-29 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_comment_status_alter_music_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('pending', 'Pending'), ('declined', 'Declined')], default='pending', max_length=8),
        ),
        migrations.AlterField(
            model_name='music',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('pending', 'Pending'), ('declined', 'Declined')], default='pending', max_length=8),
        ),
    ]
