from unicodedata import name
from django.db import models

class Musicdata(models.Model):
    acousticness = models.FloatField()
    artists = models.TextField()
    danceability = models.FloatField()
    duration_ms = models.FloatField()
    energy = models.FloatField()
    explicit = models.FloatField()
    id = models.TextField(primary_key=True)
    instrumentalness = models.FloatField()
    key = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    mode = models.FloatField()
    name = models.TextField()
    popularity = models.FloatField()
    release_date = models.IntegerField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    valence = models.FloatField()
    year = models.IntegerField()

class Playlist(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    description = models.CharField(max_length=144, default="Playlist")
    songs = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def add_song(self, song_id):
        self.songs = song_id + ":" + self.songs
        self.save()

    def remove_song(self, song_id):
        currSongs = self.parse_ids()
        self.songs = ""
        for c in currSongs:
            if c != song_id:
                self.songs = c + ":" + self.songs
        self.save()

    def parse_ids(self):
        return self.songs.split(":")

    def song_names(self):
        ids = self.parse_ids()
        names = []
        for id in ids:
            query = Musicdata.objects.filter(id=id)
            for name in query.values_list('name'):
                names.append(name[0])
        return names

    def song_artists(self):
        ids = self.parse_ids()
        artists = []
        for id in ids:
            query = Musicdata.objects.filter(id=id)
            for artist in query.values_list('artists'):
                artists.append(artist[0])
        return artists

    def song_duration(self):
        ids = self.parse_ids()
        durations = []
        for id in ids:
            query = Musicdata.objects.filter(id=id)
            for duration in query.values_list('duration_ms'):
                ms = int(duration[0])
                sec = int(ms / 1000)
                min = int(sec / 60)
                durations.append(str(min) + ":" + str(sec % 60))
        return durations