from django.contrib import admin
from .models import Music,Comment,Ban, Genre

# Register your models here.
admin.site.register(Music)
admin.site.register(Comment)
admin.site.register(Ban)
admin.site.register(Genre)
