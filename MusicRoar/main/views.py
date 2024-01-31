from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import RegisterForm, MusicForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Music, Like, Comment, User


# Create your views here.
def home(request):
    return render(request, 'main/Home.html')


@login_required(login_url='/login')
def explore(request):
    musics = Music.objects.filter(status=Music.Status.ACCEPTED)
    return render(request, 'main/Explore.html', {"musics": musics})


@login_required(login_url='/login')
def music_profile(request, musicId):
    music = Music.objects.get(id=musicId)
    comments = Comment.objects.filter(music=music)
    try:
        like = Like.objects.get(music=music, author=request.user)
        if like.isLiked:
            isLiked = True
        else:
            isLiked = False
    except Like.DoesNotExist:
        isLiked = False
    numberOfLikes = Like.objects.filter(music=music, isLiked=True).count()
    comment_form = CommentForm()
    context = {
        "music": music,
        "comments": comments,
        "isLiked": isLiked,
        "numberOfLikes": numberOfLikes,
        "comment_form": comment_form
    }
    return render(request, 'main/SongProfile_.html', context)


@login_required(login_url="/login")
def myProfile(request):
    if request.method == "POST":
        form = MusicForm(request.POST)
        if form.is_valid():
            music = form.save(commit=False)
            music.author = request.user
            music.likes = 0
            music.save()
            return redirect('/my-profile')
    else:
        form = MusicForm()
    musics = Music.objects.filter(author=request.user)
    return render(request, 'main/myProfile.html', {"form": form, "musics":musics})

@login_required(login_url="/login")
def usersPage(request):
    users = User.objects.all()
    return render(request, 'main/UsersPage.html', {"users": users})


@login_required(login_url="/login")
def userPage(request, userId):
    selectedUser = get_object_or_404(User, id=userId)
    if request.user.is_staff or request.user == selectedUser:
        musics = Music.objects.filter(author=selectedUser)
    else:
        musics = Music.objects.filter(author=selectedUser, status=Music.Status.ACCEPTED)
    return render(request, 'main/UserPage.html', {"selectedUser": selectedUser, "musics": musics})


@login_required(login_url="/login")
def edit_music(request, musicId):
    music = get_object_or_404(Music, id=musicId)

    if request.user != music.author:
        return HttpResponseForbidden("You don't have permission to edit this music.")

    if request.method == "POST":
        form = MusicForm(request.POST, instance=music)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
    else:
        form = MusicForm(instance=music)

    return render(request, 'main/editMusic.html', {'form': form, 'music': music})

@login_required(login_url='/login')
def delete_music(request,musicId):
    post = Music.objects.get(id=musicId)
    if request.user == post.author:
        post.delete()
    form = MusicForm()
    musics = Music.objects.filter(author=request.user)
    return render(request, 'main/myProfile.html', {"form": form, "musics":musics})


@login_required(login_url="/login")
def like_music(request, musicId):
    music = Music.objects.get(id=musicId)
    try:
        like = Like.objects.get(music=music, author=request.user)
        isLiked = like.isLiked
        if isLiked:
            like.isLiked = False
        else:
            like.isLiked = True
        like.save()
    except Like.DoesNotExist:
        like = Like(music=music, author=request.user, isLiked=True)
        like.save()
    return redirect('music_profile', musicId=music.id)



@login_required(login_url="/login")
def comment_music(request, musicId):
    music = Music.objects.get(id=musicId)
    received_comment_form = CommentForm(request.POST)
    if received_comment_form.is_valid():
        comment = received_comment_form.save(commit=False)
        comment.music = music
        comment.author = request.user
        comment.save()
    return redirect('music_profile', musicId=music.id)


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/my-profile')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


@login_required(login_url="/login")
def accept_music(request, musicId):
    music = Music.objects.get(id=musicId)
    music.status = music.Status.ACCEPTED
    music.save()
    return redirect('userPage', userId=music.author.id)


@login_required(login_url="/login")
def decline_music(request, musicId):
    music = Music.objects.get(id=musicId)
    music.status = music.Status.DECLINED
    music.save()
    return redirect('userPage', userId=music.author.id)

@login_required(login_url="/login")
def accept_comment(request, commentId):
    comment = Comment.objects.get(id=commentId)
    comment.status = Comment.Status.ACCEPTED
    comment.save()
    return redirect('music_profile', musicId=comment.music.id)


@login_required(login_url="/login")
def decline_comment(request, commentId):
    comment = Comment.objects.get(id=commentId)
    comment.status = Comment.Status.DECLINED
    comment.save()
    return redirect('music_profile', musicId=comment.music.id)


@login_required(login_url="/login")
def adminPage(request):
    comments = Comment.objects.filter(status=Comment.Status.PENDING)
    musics = Music.objects.filter(status=Music.Status.PENDING)
    context = {
        "comments": comments,
        "musics": musics
    }
    return render(request, 'main/AdminPage.html', context)



@login_required(login_url="/login")
def ban_user(request, userId):
    user = User.objects.get(userId)

