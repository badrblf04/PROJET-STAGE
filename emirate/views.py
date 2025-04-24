from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from django.http import HttpResponse

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/admin/')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'emirate/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            if password1 != password2:
                return render(request, 'register.html', {'form': form, 'error': 'Passwords do not match.'})

            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            # Redirection vers la page de connexion avec un message de succès
            return redirect('/login?registration_success=True')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        # Handle the forgot password logic here
        return HttpResponse("Password reset link sent.")
    return render(request, 'emirate/forgot_password.html')


from .models import Tac

def tac_report(request):
    object_list = Tac.objects.all()  # Fetch all Tac objects
    return render(request, 'tac_report.html', {'object_list': object_list})