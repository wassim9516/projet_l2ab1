from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import  Benevole
from .forms import (
    BenevoleForm,
    CustomUserRegistrationForm,
    CustomAuthenticationForm,
   
)
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def espace_perso(request):
    user = request.user
    benevole = get_object_or_404(Benevole, user=user)
    return render(request, 'benvoplanify/espace_perso.html', {'benevole': benevole})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('espace_perso')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'benvoplanify/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home_view')

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Benevole.objects.create(
                user=user,
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                email=form.cleaned_data['email'],
                date_naiss=form.cleaned_data['date_naiss']
            )
            auth_login(request, user)
            return redirect('success')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'benvoplanify/register.html', {'form': form})

@login_required
def modif_benev(request):
    user = request.user
    benevole = get_object_or_404(Benevole, user=user)
    if request.method == 'POST':
        form = BenevoleForm(request.POST, instance=benevole)
        if form.is_valid():
            form.save()
            return redirect('espace_perso')
    else:
        form = BenevoleForm(instance=benevole)
    return render(request, 'benvoplanify/modif_benev.html', {'form': form})

def success(request):
    return render(request, 'benvoplanify/success.html')

def home_view(request):
    return render(request, 'benvoplanify/home.html')
