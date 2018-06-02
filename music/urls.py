from django.conf.urls import url
from . import views

app_name = "music"    #used for namespacing. i.e; while removing harcoded url using name in urls.py many apps can have same name. So distinguish between them namespacing is used.

urlpatterns = [
	url(r'^$' , views.index , name = "index"),
	#url(r'^abcd/$' , views.index , name = "try"),
	url(r'^register/$',views.UserFormView.as_view(),name='register'),
	url(r'^(?P<album_id>[0-9]+)/$' , views.detail , name = "detail"),
	url(r'^(?P<album_id>[0-9]+)/favourite/$' , views.favourite , name = "favourite"),
	#/music/album/add
	url(r'^album/add/$', views.AlbumCreate.as_view(), name='album-add'),
	url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
]