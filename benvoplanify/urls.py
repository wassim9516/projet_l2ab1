from django.contrib import admin
from django.urls import include, path
from benvoplanify import views  
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.event_list, name='event_list'),  
    path('event/<int:id>/', views.event_detail, name='event_detail'),  
    path('event/new/', views.event_create, name='event_create'),  
    path('event/<int:id>/edit/', views.event_edit, name='event_edit'),  
    path('event/<int:id>/delete/', views.event_delete, name='event_delete'),  
    path('semaine/', views.planning_semaine, name='planning_semaine'),
    path('test/', views.test_view, name='test_views'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('espace-personnel/', views.espace_perso, name='espcace_perso'),
    path('modifier-benevole/',views.modif_benev, name='modif_benev'),
    path('login/',views.login_view, name='login'),
    path('generer_planning/',views.generer_planning,name='generer_planning'),
]
