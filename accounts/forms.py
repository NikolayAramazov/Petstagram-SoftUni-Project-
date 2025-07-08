from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile, Message


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"{username} already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"{email} is already registered.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['password1', 'password2']:
            self.fields[field_name].help_text = None
            placeholder = 'Create password' if field_name == 'password1' else 'Repeat password'
            self.fields[field_name].widget.attrs['placeholder'] = placeholder

        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'

class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
    )

    profile_img = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'img_button'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search',
            'autocomplete': 'off',
        }),
    )

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message

        fields = ['content']
