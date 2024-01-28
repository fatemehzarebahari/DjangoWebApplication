from django.shortcuts import render, redirect
from .forms import RegisterForm, MusicForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Music, Like, Comment


# Create your views here.
def home(request):
    return render(request, 'main/Home.html')


@login_required(login_url='/login')
def explore(request):
    musics = Music.objects.all()
    return render(request, 'main/Explore.html', {"musics": musics})


@login_required(login_url='/login')
def delete_music(request,musicId):
    post = Music.objects.get(id=musicId)
    if request.user == post.author:
        post.delete()
    form = MusicForm()
    musics = Music.objects.filter(author=request.user)
    return render(request, 'main/myMusics.html', {"form": form, "musics":musics})


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
    return render(request, 'main/MusicProfile.html', context)


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
    comments = Comment.objects.filter(music=music)
    numberOfLikes = Like.objects.filter(music=music, isLiked=True).count()
    comment_form = CommentForm()
    print("==================== number of likes:"+str(numberOfLikes))
    context = {
        "music": music,
        "comments": comments,
        "isLiked": like.isLiked,
        "numberOfLikes": numberOfLikes,
        "comment_form": comment_form
    }
    return render(request, 'main/MusicProfile.html', context)


@login_required(login_url="/login")
def comment_music(request, musicId):
    music = Music.objects.get(id=musicId)
    received_comment_form = CommentForm(request.POST)
    if received_comment_form.is_valid():
        comment = received_comment_form.save(commit=False)
        comment.music = music
        comment.author = request.user
        comment.save()

    comments = Comment.objects.filter(music=music)
    numberOfLikes = Like.objects.filter(music=music, isLiked=True).count()
    comment_form = CommentForm()
    try:
        like = Like.objects.get(music=music, author=request.user)
        if like.isLiked:
            isLiked = True
        else:
            isLiked = False
    except Like.DoesNotExist:
        isLiked = False

    context = {
        "music": music,
        "comments": comments,
        "isLiked": isLiked,
        "numberOfLikes": numberOfLikes,
        "comment_form": comment_form
    }
    return render(request, 'main/MusicProfile.html', context)


@login_required(login_url="/login")
def myMusics(request):
    if request.method == "POST":
        form = MusicForm(request.POST)
        if form.is_valid():
            music = form.save(commit=False)
            music.author = request.user
            music.likes = 0
            music.save()
            return redirect('/home')
    else:
        form = MusicForm()
    musics = Music.objects.filter(author=request.user)
    return render(request, 'main/myMusics.html', {"form": form, "musics":musics})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
