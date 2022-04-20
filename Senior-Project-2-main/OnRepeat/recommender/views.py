from pickle import NONE
from re import A
from recommender.forms import SearchForm, ListForm
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from .models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET
import random
#used for registration 
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
#used for Login
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render(request, 'recommender/home.html')

def find_albums(artist, from_year = None, to_year = None):
    query = Musicdata.objects.filter(artists__contains = artist)
    if from_year is not None:
        query = query.filter(year__gte = from_year)
    if to_year is not None:
        query = query.filter(year__lte = to_year)
    return list(query.order_by('-popularity').values('id','name','year'))
    

@require_POST
def searchform_post(request):
    # create a form instance and populate it with data from the request:
    form = SearchForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        from_year = None if form.cleaned_data['from_year'] == None else int(form.cleaned_data['from_year'])
        to_year = None if form.cleaned_data['to_year'] == None else int(form.cleaned_data['to_year'])
        albums = find_albums(
                form.cleaned_data['artist'],
                from_year,
                to_year
            )
        
        # Random 3 of top 10 popular albums
        answer = albums[:10]
        random.shuffle(answer)
        answer = list(answer)[:3] 
        playlists = Playlist.objects.all
        return render(request, 'recommender/searchform.html', {'form': form, 'albums': answer, 'playlists': playlists })
    else:
        raise Http404('Something went wrong')


@require_GET
def searchform_get(request):
    form = SearchForm()
    return render(request, 'recommender/searchform.html', {'form': form})

#User registration
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('home')
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="recommender/register.html", context={"register_form":form})
#User Login
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('home')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="recommender/login.html", context={"login_form":form})

#User Logout
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

#Build new playlist
def playlist_builder(request):
    # Create a new playlist form
    if request.method == 'POST':
        form = ListForm(request.POST or None)
        # check whether its valid
        if form.is_valid():
            form.save()
            playlists = Playlist.objects.all
            return render(request, 'playlist_builder.html', {'playlists': playlists})
        else:
            print(form.errors)
            raise Http404('Post form not valid')
    else:
        playlists = Playlist.objects.all
        return render(request, 'recommender/playlist_builder.html', {'playlists': playlists})

#Delete existing playlist
def delete_playlist(request, playlist_name):
    playlist = Playlist.objects.get(pk=playlist_name)
    playlist.delete()
    return redirect('playlist_builder')

def add_song(request):
    form = AddSongForm(request.POST or None)
    if form.is_valid():
        playlist_name = form.cleaned_data['playlist_name']
        song_id = form.cleaned_data['song_id']
        playlist = Playlist.objects.get(pk=playlist_name)
        playlist.add_song(song_id)
        return redirect('recommender:best')
    else:
        print(form.errors)
        raise Http404('Post form not valid')

def remove_song(request):
    form = AddSongForm(request.POST or None)
    if form.is_valid():
        playlist_name = form.cleaned_data['playlist_name']
        song_id = form.cleaned_data['song_id']
        playlist = Playlist.objects.get(pk=playlist_name)
        playlist.remove_song(song_id)
        playlists = Playlist.objects.all
        return render(request, 'recommender/playlist_builder.html', {'playlists': playlists})
    else:
        print(form.errors)
        raise Http404('Post form not valid')