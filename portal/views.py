from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from portal.models import Song, Group, Turn
from portal.forms import SongForm

@login_required
def portal_main_page(request):
    """
    If users authenticated, direct them to main page. Otherwise take
    them to login page.
    """
    return render(request, 'portal/index.html', 
        context_instance=RequestContext(request))

@login_required
def my_songs_page(request):
    """
    If users authenticated, direct to my songs page. Otherwise take
    them to login page.
    """
    songs = Song.objects.all().filter(recommender=request.user)
    return render(request, 'portal/mysongs.html',
        {"songs": songs},
        context_instance=RequestContext(request))
    
@login_required
def add_song_page(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['name']
            furl = form.cleaned_data['url']
            
            s = Song.objects.create(name=fname, url=furl,
                recommender=request.user)
            
            return HttpResponseRedirect('/portal/mysongs/')
            
    else:
        form = SongForm()
        
    return render(request, 'portal/addsong.html', {'form': form})
    
@login_required
def remove_song(request, id):
    s = Song.objects.get(pk=id)
    if s:
        s.delete()
    return HttpResponseRedirect('/portal/mysongs/')
    
    