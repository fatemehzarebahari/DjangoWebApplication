from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Music(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio/', null=True)
    likes = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title + "\n" + self.author.username