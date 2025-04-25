from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, get_user_model, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import  Benevole,JOURS,CRENEAUX,Indisponibilite,EmploiDuTemps,Message
from django.forms import modelformset_factory
from .forms import BenevoleForm,CustomUserRegistrationForm,CustomAuthenticationForm,MessageForm
from django.contrib import messages


User = get_user_model()

@login_required
def emploi_du_temps_view(request):
    jours = [(0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')]
    creneaux = [(8, '08h - 10h'), (10, '10h - 12h'), (12, '12h - 14h'), (14, '14h - 16h'), (16, '16h - 18h')]

    # On crée une structure de dictionnaire pour afficher les bénévoles affectés à chaque créneau
    emploi_du_temps = {j[0]: {c[0]: [] for c in creneaux} for j in jours}

    # On parcourt toutes les affectations pour remplir l'emploi du temps
    for affectation in EmploiDuTemps.objects.select_related('benevole'):
        jour = affectation.jour
        creneau = affectation.creneau
        benevole = affectation.benevole
        emploi_du_temps[jour][creneau].append(f"{benevole.prenom} {benevole.nom}")

    return render(request, 'benvoplanify/emploi_du_temps.html', {
        'emploi_du_temps': emploi_du_temps,
        'jours': jours,
        'creneaux': creneaux
    })



from django.contrib import messages

@login_required
def indisponibilite_view(request):
    user = request.user
    benevole = get_object_or_404(Benevole, user=user)

    if request.method == 'POST':
        # Supprimer les anciennes indisponibilités de ce bénévole
        Indisponibilite.objects.filter(benevole=benevole).delete()

        for jour in range(7):
            toute_journee = request.POST.get(f"jour_{jour}_toute_journee") == "on"
            for creneau in [8, 10, 12, 14, 16]:
                if toute_journee or request.POST.get(f"{jour}_{creneau}") == "on":
                    Indisponibilite.objects.create(benevole=benevole, jour=jour, creneau=creneau)

        # Génération automatique du planning avec maximum 3 bénévoles par créneau
        EmploiDuTemps.objects.filter(benevole=benevole).delete()

        indispo = {(i.jour, i.creneau) for i in Indisponibilite.objects.filter(benevole=benevole)}
        heures_attribuees = 0
        planning_genere = []

        for jour in range(7):
            for creneau in [8, 10, 12, 14, 16]:
                if (jour, creneau) not in indispo:
                    count = EmploiDuTemps.objects.filter(jour=jour, creneau=creneau).count()
                    if count < 3:
                        EmploiDuTemps.objects.create(benevole=benevole, jour=jour, creneau=creneau)
                        heures_attribuees += 2
                        planning_genere.append((jour, creneau))
                        if heures_attribuees >= 20:
                            break
            if heures_attribuees >= 20:
                break

        return render(request, 'benvoplanify/indisponibilites.html', {
            'jours': JOURS,
            'creneaux': CRENEAUX,
            'planning_genere': planning_genere,
            'heures': heures_attribuees,
        })

    return render(request, 'benvoplanify/indisponibilites.html', {
        'jours': JOURS,
        'creneaux': CRENEAUX,
    })





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

@login_required
def messagerie(request, message_id=None):
    """Gère la messagerie : affichage des messages, envoi et consultation des détails"""
    user = request.user

    # Afficher les messages reçus
    messages_reçus = Message.objects.filter(receiver=user).order_by('-timestamp')

    # Consultation des détails d'un message
    message_detail = None
    if message_id:
        message_detail = get_object_or_404(Message, id=message_id, receiver=user)
        message_detail.is_read = True
        message_detail.save()

    # Envoi d'un nouveau message
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.save()
            messages.success(request, "Message envoyé avec succès.")
            return redirect('messagerie')
    else:
        form = MessageForm()

    return render(request, 'benvoplanify/messagerie.html', {
        'messages_reçus': messages_reçus,
        'message_detail': message_detail,
        'form': form,
    })
