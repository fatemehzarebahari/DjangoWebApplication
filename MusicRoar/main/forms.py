from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Music


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
        
class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'audio_file']  # Add other fields as needed

    def __init__(self, *args, **kwargs):
        super(MusicForm, self).__init__(*args, **kwargs)
        self.fields['audio_file'].widget.attrs.update({'accept': 'audio/*'})