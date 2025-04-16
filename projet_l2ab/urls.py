# projet_l2ab/urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from benvoplanify import views  # Importation de views depuis l'application 'planning'
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', lambda request: redirect('home_view')), 
    path('admin/', admin.site.urls),
    path('benvoplanify/', include('benvoplanify.urls')),
]


