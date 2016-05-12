import operator
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from portal.models import Game
    
champlist = [ 'Annie', 'Yasuo', 'Zed' ]
    
def main_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/portal/')
    return render(request, 'index.html',
        context_instance=RequestContext(request))
        
def data_page_games(request):
    data = Game.objects.all()
    cdata = dict()
    for key in champlist:
        gms = data.filter(champs__contains=key)
        wins = gms.filter(win__gt=0).count()
        cdata[key] = (gms.count(), wins)
    sorteddata = sorted(cdata.items(), key=operator.itemgetter(1), reverse=True)
 
    return render(request, 'data.html', {'d': sorteddata},
        context_instance=RequestContext(request))

def data_page_rate(request):
    data = Game.objects.all()
    cdata = dict()
    for key in champlist:
        gms = data.filter(champs__contains=key)
        wins = gms.filter(win__gt=0).count()
        cdata[key] = (gms.count(), wins)
    sorteddata = sorted(cdata.items(), key=operator.itemgetter(1).1/operator.itemgetter(1).0)
 
    return render(request, 'data.html', {'d': sorteddata},
        context_instance=RequestContext(request))

def data_page_month(request):
    t = date.today()
    start = t - timedelta(days=30)
    data = Game.objects.all().filter(date__range=[start, t])
    cdata = dict()
    for key in champlist:
        gms = data.filter(champs__contains=key)
        wins = gms.filter(win__gt=0).count()
        cdata[key] = (gms.count(), wins)
    sorteddata = sorted(cdata.items(), key=operator.itemgetter(1), reverse=True)
 
    return render(request, 'data.html', {'d': sorteddata},
        context_instance=RequestContext(request))

        
def logout_page(request):
    """
    log users out and redirect them to main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    """
    allows user to create a ddd account
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/portal/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", 
        {'form': form}, context_instance=RequestContext(request))
    
    