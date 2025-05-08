# projet_l2ab/urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
    path('', include('benvoplanify.urls')),
    path('admin/', admin.site.urls),
    path('benvoplanify/', include('benvoplanify.urls')),
]


