from django.db import models
from django.core.urlresolvers import reverse

class Album(models.Model):
	artist = models.CharField(max_length = 200)
	album_title = models.CharField(max_length = 500)
	album_logo = models.FileField()

	def get_absolute_url(self):
		return reverse('music:detail',kwargs={'pk':self.pk})

	def __str__(self):
		return self.artist + "-" + self.album_title

class Song(models.Model):
	album = models.ForeignKey(Album , on_delete = models.CASCADE)
	genre = models.CharField(max_length = 100)
	song_title = models.CharField(max_length = 300)
	is_favourite = models.BooleanField(default = False)
	file = models.FileField()    

	def __str__(self):
		return self.song_title + "."