from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    log users out and redirect them to main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

