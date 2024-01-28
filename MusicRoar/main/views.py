from django.shortcuts import render, redirect
from .forms import RegisterForm, MusicForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Music

# Create your views here.
@login_required(login_url='/login')
def home(request):
    musics = Music.objects.all()
    
    if request.method == "POST":
        musicId = request.POST.get("delete-music")
        post = Music.objects.get(id=musicId)
        if request.user == post.author:
            post.delete()
        
    return render(request, 'main/home.html', {"musics": musics})


@login_required(login_url="/login")
def upload_music(request):
    if request.method == "POST":
        form = MusicForm(request.POST)
        if form.is_valid():
            music = form.save(commit=False)
            music.author = request.user
            music.save()
            return redirect('/home')
    else:
        form = MusicForm()
    
    return render(request, 'main/create_music.html', {"form": form})


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
    