from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Music,Comment,Genre
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'audio_file', 'genre']

    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select,
        required=False,
        empty_label="Select a genre"
    )

    def __init__(self, *args, **kwargs):
        super(MusicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Changes'))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class DeleteGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre']

    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select,
        required=False,
        empty_label="Select a genre"
    )