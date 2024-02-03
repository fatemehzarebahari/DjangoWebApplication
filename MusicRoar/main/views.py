from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import RegisterForm, MusicForm, CommentForm, GenreForm, DeleteGenreForm, MusicSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import History, Music, Like, Comment, User,Ban, View, Genre
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request, 'main/Home.html')


@login_required(login_url='/login')
def explore(request):
    form = MusicSearchForm(request.GET)

    banned_users = Ban.objects.values('user')
    musics = Music.objects.filter(
        status=Music.Status.ACCEPTED
    ).exclude(author__id__in=banned_users)

    searchItem = request.GET.get('search-area') or ""
    if searchItem:
        musics = musics.filter(
            Q(title__icontains=searchItem) | Q(author__username__icontains=searchItem)
        )
    genreItem = request.GET.get('genre-area') or ""
    if genreItem == "clear":
        musics = musics.all()
    else:
        if genreItem:
            musics = musics.filter(
                Q(Q(genre__name__icontains=genreItem))
            )
    genres = Genre.objects.all()
    content = {
        "musics": musics,
        'searchItem': searchItem,
        'genreItem': genreItem,
        "genres": genres
    }

    return render(request, 'main/Explore.html', content)

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
        
    view = View.objects.filter(music=music, author=request.user)
    if not view.exists():
        View.objects.create(music=music, author=request.user)
        
    History.objects.create(music=music, user=request.user, action="viewed")
    
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
def myProfile(request):
    if request.method == "POST":
        form = MusicForm(request.POST, request.FILES)
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
    banned_users = Ban.objects.values('user')
    users = User.objects.exclude(id__in=banned_users)
    return render(request, 'main/UsersPage.html', {"users": users})


@login_required(login_url="/login")
def userPage(request, userId):
    selectedUser = get_object_or_404(User, id=userId)
    if request.user.is_staff or request.user == selectedUser:
        musics = Music.objects.filter(author=selectedUser)
    else:
        musics = Music.objects.filter(author=selectedUser, status=Music.Status.ACCEPTED)
    try:
        ban_instance = Ban.objects.get(user=selectedUser)
        is_banned = True
    except Ban.DoesNotExist:
        is_banned = False
    print(is_banned)
    
    histories = selectedUser.history_set.all().order_by('-timestamp')
    
    context = {
    "selectedUser": selectedUser,
    "musics": musics,
    "is_banned": is_banned,
    "histories": histories
    }
    return render(request, 'main/UserPage.html', context)


@login_required(login_url="/login")
def edit_music(request, musicId):
    music = get_object_or_404(Music, id=musicId)

    if request.user != music.author and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to edit this music.")

    if request.method == "POST":
        form = MusicForm(request.POST, instance=music)
        if form.is_valid():
            form.save()
            return redirect('explore')
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
        
    History.objects.create(music=music, user=request.user, action="liked")
    
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
        History.objects.create(music=music, user=request.user, action="commented")
        
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
    banned_users = Ban.objects.all()
    form = GenreForm()
    delete_genre_form = DeleteGenreForm()
    context = {
        "comments": comments,
        "musics": musics,
        "banned_users": banned_users,
        "genre_form": form,
        "delete_genre_form": delete_genre_form
    }
    return render(request, 'main/adminPage_.html', context)


@login_required(login_url="/login")
def ban_user(request, userId):
    if request.user.is_staff:
        selected_user = get_object_or_404(User, id=userId)

        if not Ban.objects.filter(user=selected_user).exists():
            Ban.objects.create(user=selected_user, reason='Violation of terms')
        else:
            Ban.objects.get(user=selected_user).delete()

    return redirect('userPage', userId=selected_user.id)


def most_liked(request):
    sortedMusics = sorted(Music.objects.filter(status=Music.Status.ACCEPTED), key=lambda x: x.like_count(), reverse=True)
    genres = Genre.objects.all()
    return render(request, 'main/Explore.html', {"musics": sortedMusics,"genres": genres})

def most_commented(request):
    sortedMusics = sorted(Music.objects.filter(status=Music.Status.ACCEPTED), key=lambda x: x.comment_count(), reverse=True)
    genres = Genre.objects.all()
    return render(request, 'main/Explore.html', {"musics": sortedMusics,"genres":genres})

def most_viewed(request):
    sortedMusics = sorted(Music.objects.filter(status=Music.Status.ACCEPTED), key=lambda x: x.view_count(), reverse=True)
    genres = Genre.objects.all()
    return render(request, 'main/Explore.html', {"musics": sortedMusics,"genres": genres})


@login_required(login_url="/login")
def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('adminPage')


@login_required(login_url="/login")
def delete_genre(request):
    if request.method == 'POST':
        form = DeleteGenreForm(request.POST)
        if form.is_valid():
            genre = form.cleaned_data['genre']
            if genre:
                genre.delete()
    return redirect('adminPage')

