from django.db import models
from django.urls import reverse ,reverse_lazy
from django.contrib.auth.models import User, Permission
class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    album_artist = models.CharField(max_length=255)
    album_title = models.CharField(max_length=500)
    album_genre = models.CharField(max_length=200)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_artist + ' - ' +self.album_title

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title



