from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('my-profile/', views.myProfile, name='my-profile'),
    path('view-music/<int:musicId>', views.music_profile, name='music_profile'),
    path('like_music/<int:musicId>', views.like_music, name='like_music'),
    path('comment_music/<int:musicId>', views.comment_music, name='comment_music'),
    path('delete_music/<int:musicId>', views.delete_music, name='delete_music'),
    path('edit_music/<int:musicId>', views.edit_music, name='edit_music'),
    path('usersPage', views.usersPage, name='usersPage'),
    path('userPage/<int:userId>', views.userPage, name='userPage'),
    path('decline-music/<int:musicId>', views.decline_music, name='decline-music'),
    path('accept-music/<int:musicId>', views.accept_music, name='accept-music'),
    path('decline-comment/<int:commentId>', views.decline_comment, name='decline-comment'),
    path('accept-comment/<int:commentId>', views.accept_comment, name='accept-comment'),
    path('adminPage', views.adminPage, name='adminPage'),
    path('ban-user/<int:userId>/', views.ban_user, name='ban-user'),
    path('most-liked', views.most_liked, name='most-liked'),
    path('most-commented', views.most_commented, name='most-commented'),
    path('most-viewed', views.most_viewed, name='most-viewed'),
    path('add-genre', views.add_genre, name="add-genre"),
    path('delete-genre/', views.delete_genre, name="delete-genre"),
    path('genre_detail/<int:genreId>', views.genre_detail, name="genre_detail")
]