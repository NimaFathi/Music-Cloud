from django.http import Http404
from django.http import  HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Album, Song
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, SongForm
from django.http import JsonResponse
from django.db.models import Q
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

'''
def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums}
    return render(request, 'music/index.html', context)
def detail(request, album_id):
    #try:
     #   album = Album.objects.get(pk=album_id)
    #except Album.DoesNotExist:
     #   raise Http404("Album does not exist")
    # instead:
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album})
'''
def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selectes_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {
            'album': album,
            'error_message': "Song Not valid!",
        })
    else:
        if(selectes_song.is_favorite == False):
            selectes_song.is_favorite = True
        else:
            selectes_song.is_favorite = False
        selectes_song.save()
        return render(request, 'music/detail.html', {'album': album,
        })

class IndexView (generic.ListView):
    template_name = 'music/index.html'
    context_object_name = "all_albums"
    def get_queryset(self):
        return Album.objects.all()
class DetailView (generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate (CreateView):
    model = Album
    fields = ['album_artist', 'album_title', 'album_genre', 'album_logo']
class AlbumUpdate (UpdateView):
    model = Album
    fields = ['album_artist', 'album_title', 'album_genre', 'album_logo']
class AlbumDelete(DeleteView):
    model = Album
    fields = ['album_artist', 'album_title', 'album_genre', 'album_logo']
    success_url = reverse_lazy('music:index')
class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display a blank for before sign up

    def get(self, request):
        form = self.form_class(None)
        return render(request , self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # store locally
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return user objects if credentials are OK
            user = authenticate(username=username, password=password)
            if user is not None:
                # user not ban
                if user.is_active:
                    login(request,user)
                    # get user name:
                    #request.user.username ...
                    return redirect('music:index')

        return render(request, self.template_name, {'form':form})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')




def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })
def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})