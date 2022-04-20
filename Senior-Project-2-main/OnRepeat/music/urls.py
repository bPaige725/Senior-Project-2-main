"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from recommender import views
from recommender.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recommender/', include('recommender.urls')),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path('logout', views.logout_request, name="logout"),
    path('home/', views.home, name='home'),
    path('playlist_builder/', views.playlist_builder, name='playlist_builder'),
    path('delete_playlist/<playlist_name>', views.delete_playlist, name='delete_playlist'),
    path('add_song/', views.add_song, name='add_song'),
    path('best/', views.searchform_get, name='best'),
    path('',include('Discussion_Forum.urls')),
    path('remove_song/', views.remove_song, name='remove_song'),
]
