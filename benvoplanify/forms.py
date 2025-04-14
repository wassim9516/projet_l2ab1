# planning/forms.py
from django import forms
from .models import Event, CustomUser
from django.contrib.auth.models import User
from .models import Benevole
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time','location']

class BenevoleForm(forms.ModelForm):
    class Meta:
        model = Benevole
        fields = ['nom', 'prenom', 'email', 'date_naiss']
        widgets = {
            'date_naiss': forms.DateInput(attrs={'type': 'date'}),  
        }

class CustomUserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = get_user_model()
        fields = ['email', 'nom', 'prenom', 'date_naiss']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Définit le mot de passe de l'utilisateur
        if commit:
            user.save()
        return user
    