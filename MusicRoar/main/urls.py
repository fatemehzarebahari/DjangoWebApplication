from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('my-musics/', views.myMusics, name='my-musics'),
    path('view-music/<int:musicId>', views.music_profile, name='music_profile'),
    path('like_music/<int:musicId>', views.like_music, name='like_music'),
    path('comment_music/<int:musicId>', views.comment_music,name='comment_music'),
    path('delete_music/<int:musicId>', views.delete_music, name='delete_music')

]