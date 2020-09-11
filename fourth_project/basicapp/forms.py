from django import forms
from django.contrib.auth.models import User
from basicapp.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('site', 'profile_pic')

class Login_Form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        all_clean_data = super().clean()
