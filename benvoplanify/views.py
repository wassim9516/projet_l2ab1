# planning/views.py
from os import login_tty
from django.shortcuts import render, redirect,get_object_or_404
from .models import Event
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Créer l'utilisateur
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)  # Connexion automatique après inscription
            return redirect('event_list')  # Rediriger vers la liste des événements
    else:
        form = UserCreationForm()  # Afficher un formulaire vide

    return render(request, 'benvoplanify/register.html', {'form': form})


def event_list(request):
    events = Event.objects.all()  # Récupère tous les événements
    paginator = Paginator(events, 6)  # 6 événements par page
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
    """ Affiche les détails d'un événement """
    event = get_object_or_404(Event, id=id)
    return render(request, 'benvoplanify/detail.html', {'event': event})

def event_delete(request, id):
    """ Supprime un événement """
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'benvoplanify/event_confirm_delete.html', {'event': event})

def event_edit(request, id):
    """ Modifie un événement existant """
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', id=id)
    else:
        form = EventForm(instance=event)
    return render(request, 'benvoplanify/event_form.html', {'form': form})
