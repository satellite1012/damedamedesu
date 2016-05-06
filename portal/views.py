from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from portal.models import Game
from portal.forms import AddGameForm

@login_required
def portal_main_page(request):
    """
    If users authenticated, direct them to main page. Otherwise take
    them to login page.
    """    
    
    return render(request, 'portal/index.html', 
        {}, 
        context_instance=RequestContext(request))

@login_required
def add_game_page(request):
    if request.method == 'POST':
        form = AddGameForm(request.POST, mlist=mlist)
        if form.is_valid():
            fday = form.cleaned_data['day']
            fchamps = "%s/%s/%s/%s/%s" % (form.cleaned_data['champ1'], form.cleaned_data['champ2'], form.cleaned_data['champ3'], form.cleaned_data['champ4'], form.cleaned_data['champ5'])
                            
            # check that url hasn't been used already
            g = Game.objects.create(day=fday, champions=fchamps)
            
            return HttpResponseRedirect('/portal/')
            
    else:
        form = AddGameForm()
        
    return render(request, 'portal/addgame.html', {'form': form})
    