from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import UserForm
from django.http import HttpResponse,Http404
from django.template import loader
from .models import Album,Song
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy

def index(request):
	all_albums = Album.objects.all()
	#template = loader.get_template('Music/index.html')
	context = {
		'all_albums' : all_albums,
	}
	return render(request , 'music/index.html' , context)

def detail(request , album_id):
	'''try:
		album = Album.objects.get(pk = album_id)
	except Album.DoesNotExist:
		raise Http404("This page does not exist")'''
	album = get_object_or_404(Album , pk = album_id)
	return render(request , 'music/detail.html' , {'album' : album})


def favourite(request,album_id):
	album = get_object_or_404(Album , pk = album_id)
	try:
		selected_song = album.song_set.get(pk=request.POST['song'])  #this method of providing pk works for radio but for checkbox the latest selected one is only favourited
	except(KeyError,Song.DoesNotExist):
		return render(request,'music/detail.html',{'album':album,'error_message':"You did not select a valid song"})
	else:
		selected_song.is_favourite = True
		selected_song.save()	
		return render(request,'music/detail.html',{'album':album})

class AlbumCreate(CreateView):
	model = Album
	fields = ['artist' , 'album_title','album_logo']
	success_url = reverse_lazy('music:index')

class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist' , 'album_title','album_logo']
	success_url = reverse_lazy('music:index')


class UserFormView(View):
	form_class = UserForm
	template_name = "music/signup.html"

	#just to display blank form
	def get(self,request):
		form = self.form_class(None)
		return render(request,self.template_name,{'form':form})

	#to handle submission of form
	def post(self,request):	
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit = False) #saves users details in user object 

			#cleaned normalised data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save() #saves user details in database

			if user is not None:
				if user.is_active:
					login(request,user)
					return redirect('music:index')
		return render(request,self.template_name,{'form':form})