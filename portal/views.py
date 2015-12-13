from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def portal_main_page(request):
    """
    If users authenticated, direct them to main page. Otherwise take
    them to login page.
    """
    return render_to_response('portal/index.html', 
        context_instance=RequestContext(request))

@login_required
def my_songs_page(request):
    """
    If users authenticated, direct to my songs page. Otherwise take
    them to login page.
    """
    return render_to_response('portal/mysongs.html',
        context_instance=RequestContext(request))
    
