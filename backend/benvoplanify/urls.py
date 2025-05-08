from django.urls import  path
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
    path('indisponibilites/',views.indisponibilite_view, name='indisponibilite_view'),
    path('emploi-du-temps/', views.emploi_du_temps_view, name='emploi_du_temps_view'),
    path('messagerie/', views.messagerie, name='messagerie'),
    path('api/hello/',views.hello,name='hello'),
    path('api/benevoles/',views.benevoles_list,name='benvevoles_list')
]
