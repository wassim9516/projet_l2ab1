from django.contrib import admin
from django.urls import include, path
from benvoplanify import views  # Importation de views depuis l'application 'planning'
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.event_list, name='event_list'),  # Page principale
    path('event/<int:id>/', views.event_detail, name='event_detail'),  # Détails d'un événement
    path('event/new/', views.event_create, name='event_create'),  # Création d'un événement
    path('event/<int:id>/edit/', views.event_edit, name='event_edit'),  # Modification d'un événement
    path('event/<int:id>/delete/', views.event_delete, name='event_delete'),  # Suppression d'un événement
]