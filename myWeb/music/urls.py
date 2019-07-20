from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    #/music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    #/music/?albumID/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /music/?albumID/favorite
    url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),

    # /music/album/add/
    url(r'^album/add/$' , views.AlbumCreate.as_view(), name='album-add'),

    # /music/album/pk/
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    # /music/album/pk/delete/
    url(r'^album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='delete_album'),

    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),

    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),

    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),

url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),

url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

]