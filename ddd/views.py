import operator
from datetime import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from portal.models import Game
    
champlist = [ 'Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Ashe', 'Aurelion Sol', 'Azir', 
'Bard', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 
'Dr. Mundo', 'Draven', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 
'Gangplank', 'Garne', 'Gnar', 'Gragas', 'Graves', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Janna', 
'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 
'Kayle', 'Kennen', 'Khazix', 'Kindred', 'Kogmaw', 'LeBlanc', 'Lee Sin', 'Leona', 'Lissandra', 'Lucian', 
'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'Master Yi', 'Miss Fortune', 'Mordekaiser', 'Morgana', 'Nami', 
'Nasus', 'Nautilus', 'Nidalee', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Pantheon', 'Poppy', 'Quinn', 
'Rammus', 'Reksai', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Sejuani', 'Shaco', 'Shen', 
'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Syndra', 'Tahn Kench', 
'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 
'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vi', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 
'Wukong', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yorick', 'Zac', 'Zed', 'Ziggs', 'Zilean', 'Zyra' ]
    
def main_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/portal/')
    return render(request, 'index.html',
        context_instance=RequestContext(request))
        
def data_page_games(request):
    data = Game.objects.all()
    tgames = Game.objects.count()
    cdata = dict()
    for key in champlist:
        gms = data.filter(champs__contains=key)
        wins = gms.filter(win__gt=0).count()
        if gms.count() > 0:
            rate = 100.0*wins/gms.count()
            cdata[key] = (gms.count(), wins, rate)
    sorteddata = sorted(cdata.items(), key=operator.itemgetter(1), reverse=True)
 
    return render(request, 'data.html', {'d': sorteddata, 'g': tgames},
        context_instance=RequestContext(request))

def data_page_rate(request):
    data = Game.objects.all()
    tgames = Game.objects.count()
    cdata = dict()
    for key in champlist:
        gms = data.filter(champs__contains=key)
        wins = gms.filter(win__gt=0).count()
        if gms.count() > 0:
            rate = 100.0*wins/gms.count()
            cdata[key] = (gms.count(), wins, rate)
    sorteddata = sorted(cdata.items(), key=lambda x: x[1][2])
 
    return render(request, 'data.html', {'d': sorteddata, 'g': tgames},
        context_instance=RequestContext(request))

def data_page_month(request):
    t = date.today()
    start = t - timedelta(days=30)
    data = Game.objects.all().filter(day__range=[start, t])
    tgames = data.count()
    cdata = dict()
    for key in champlist:
        gms = data.filter(champs__contains=key)
        wins = gms.filter(win__gt=0).count()
        if gms.count() > 0:
            rate = 100.0*wins/gms.count()
            cdata[key] = (gms.count(), wins, rate)
    sorteddata = sorted(cdata.items(), key=operator.itemgetter(1), reverse=True)
 
    return render(request, 'data.html', {'d': sorteddata, 'g': tgames},
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
    
    