# planning/views.py
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from os import login_tty
from django.shortcuts import render, redirect,get_object_or_404
from .models import Event, Benevole
from .forms import EventForm, BenevoleForm,Benevole
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm

def login_view(request):
    """ page de connexion """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('espcace_perso')  
    else:
        form = AuthenticationForm()

    return render(request, 'benvoplanify/login.html', {'form': form})


def register(request):
    """ inscription uitlisater """
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Création de l'utilisateur
            
            # Création du profil Benevole lié à l'utilisateur
            Benevole.objects.create(
                user=user,
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                email=form.cleaned_data['email'],
                date_naiss=form.cleaned_data['date_naiss'],
            )

            # Connexion automatique après inscription
            auth_login(request, user)
            return redirect('success')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'benvoplanify/register.html', {'form': form})


@login_required
def modif_benev(request):
    """ Modif les informations utilisateur """
    user = request.user
    benevole = Benevole.objects.get(user=user)

    if request.method == 'POST':
        form = BenevoleForm(request.POST, instance=benevole)
        if form.is_valid():
            form.save()
            return redirect('espace_perso')  
    else:
        form = BenevoleForm(instance=benevole)

    return render(request, 'benvoplanify/modif_benev.html', {'form': form})


@login_required
def espace_perso(request):
    """ espace personnel """
    user = request.user
    benevole = get_object_or_404(Benevole, user=user)

    context = {
        'benevole': benevole,
    }
    return render(request, 'benvoplanify/espcace_perso.html', context)


def event_list(request):
    events = Event.objects.all()  
    paginator = Paginator(events, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'benvoplanify/event_list.html', {'page_obj': page_obj})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'benvoplanify/event_form.html', {'form': form})

def event_detail(request,id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'benvoplanify/detail.html', {'event': event})

def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'benvoplanify/event_confirm_delete.html', {'event': event})

def event_edit(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', id=id)
    else:
        form = EventForm(instance=event)
    return render(request, 'benvoplanify/event_form.html', {'form': form})


def planning_semaine(request):
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    heures = list(range(8, 20, 1))

    planning = {jour: {heure: [] for heure in heures} for jour in jours_semaine}

    events = Event.objects.all()

    for event in events:
        jour = event.start_time.strftime("%A")  
        jour = jour.capitalize()
        heure = event.start_time.hour
        if jour in planning and heure in planning[jour]:
            planning[jour][heure].append(event)

    context = {
        'days': jours_semaine,
        'hours': heures,
        'planning': planning,
    }
    return render(request, 'benvoplanify/planning_semaine.html', context)

def test_view(resquest):
    return render(resquest, 'benvoplanify/test.html')

def success(request):
    return render(request, 'benvoplanify/success.html')

def generer_planning(request):
    return render(request,'benvoplanify/generer_planning.html')



