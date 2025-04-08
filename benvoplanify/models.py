from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


    

class Event(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    user        = user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location    = models.CharField(max_length=255,blank=True, null=True)
    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time}) {self.location}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naiss = models.DateField()

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['nom', 'prenom', 'date_naiss']  

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Benevole(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relation 1-1 avec CustomUser
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_naiss = models.DateField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
