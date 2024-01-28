from django.shortcuts import render, redirect
from .forms import RegisterForm, MusicForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Music, Like, Comment


# Create your views here.
def home(request):
    return render(request, 'main/Home.html')


@login_required(login_url='/login')
def explore(request):
    musics = Music.objects.all()
    if request.method == "POST":
        musicId = request.POST.get("delete-music")
        post = Music.objects.get(id=musicId)
        if request.user == post.author:
            post.delete()
    return render(request, 'main/Explore.html', {"musics": musics})


@login_required(login_url='/login')
def user_response(request):
    return None


@login_required(login_url='/login')
def music_profile(request, musicId):
    music = Music.objects.get(id=musicId)
    comments = Comment.objects.filter(music=music)
    try:
        like = Like.objects.get(music=music, author=request.user)
        isLiked = True
    except Like.DoesNotExist:
        isLiked = False

    numberOfLikes = Like.objects.filter(music=music, isLiked=True).count()
    context = {
        "music": music,
        "comments": comments,
        "isLiked": isLiked,
        "numberOfLikes": numberOfLikes
    }
    return render(request, 'main/MusicProfile.html', context)

@login_required(login_url="/login")
def like_music(request, musicId):
    return None

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

    return render(request, 'main/myMusics.html', {"form": form})


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
