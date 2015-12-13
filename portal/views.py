from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def portal_main_page(request):
    """
    If users authenticated, direct them to main page. Otherwise take
    them to login page.
    """
    return render_to_response('portal/index.html')

@login_required
def my_songs_page(request):
    """
    If users authenticated, direct to my songs page. Otherwise take
    them to login page.
    """
    return render_to_response('portal/mysongs.html')
    
