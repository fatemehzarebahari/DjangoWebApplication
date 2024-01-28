from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Music(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio/', null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + "\n" + self.author.username


class Comment(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.music.title + "\n" + self.author.username


class Like(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isLiked = models.BooleanField()
