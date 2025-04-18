from django.contrib import admin
from django.urls import include, path
from benvoplanify import views  
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home_view'),  
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('espace-personnel/', views.espace_perso, name='espace_perso'),
    path('modifier-benevole/',views.modif_benev, name='modif_benev'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),
    
]
