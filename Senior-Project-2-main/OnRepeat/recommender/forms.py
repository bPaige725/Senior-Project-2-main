from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Playlist

class SearchForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    from_year = forms.IntegerField(required=False)
    to_year = forms.IntegerField(required=False)

 # Create your forms here.
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

#Form for playlist page
class ListForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["name" , "description", "songs"]

#Form for adding songs to playlists
class AddSongForm(forms.Form):
    playlist_name = forms.CharField()
    song_id = forms.CharField()