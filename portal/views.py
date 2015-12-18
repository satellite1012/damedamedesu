from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from portal.models import Song, Member, Group, Turn

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
    songs = Song.objects.all().filter(recommender__user=request.user)
    return render(request, 'portal/mysongs.html',
        {"songs": songs},
        context_instance=RequestContext(request))
    
