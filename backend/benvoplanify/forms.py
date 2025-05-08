from django import forms
from .models import Benevole,Indisponibilite
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import Message

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class IndisponibiliteForm(forms.ModelForm):
    class Meta:
        model = Indisponibilite
        fields = ['jour', 'creneau']


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
        model = User
        fields = ['email', 'nom', 'prenom', 'date_naiss']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email déjà existant")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        return super().confirm_login_allowed(user)

    def clean(self):
        try:
            return super().clean()
        except forms.ValidationError:
            self._errors.clear()
            self.add_error(None, "Email ou mot de passe incorrect")

