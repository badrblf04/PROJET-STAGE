# emirate/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom d\'utilisateur',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe',
    }))

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe',
    }))
    password2 = forms.CharField(label='Confirmez le mot de passe', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirmez le mot de passe',
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cd['password2']
    
   

class CustomUserCreationForm(UserCreationForm):
    is_superuser = forms.BooleanField(label='Superuser', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('is_superuser'):
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user
    


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
