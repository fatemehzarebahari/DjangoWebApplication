from django.db import models
from django.contrib.auth.models import User


class Music(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = "accepted"
        PENDING = "pending"
        DECLINED = "declined"

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio/', null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return self.title + "\n" + self.author.username + str(self.status)


class Comment(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = "accepted"
        PENDING = "pending"
        DECLINED = "declined"
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return self.music.title + "\n" + self.author.username + str(self.status)


class Like(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isLiked = models.BooleanField()


class Ban(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'
