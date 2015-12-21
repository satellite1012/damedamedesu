from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from portal.models import Song, Group, Turn
from portal.forms import SongForm, GroupForm

@login_required
def portal_main_page(request):
    """
    If users authenticated, direct them to main page. Otherwise take
    them to login page.
    """
    
    g = request.user.group_set.all()
    if not g:
        g = None
    
    return render(request, 'portal/index.html', 
        {'groups': g}, 
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
    
@login_required
def create_group_page(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            gname = form.cleaned_data['name']
            gpassword = form.cleaned_data['password']
            
            if gname and Group.objects.filter(name=gname).exclude(password=gpassword).count():
                return render(request, 'portal/creategroup.html',
                {'error': 'That group name already exists.',
                'form': form})
            
            g = Group.objects.create(name=gname, password=gpassword)
            g.member_list.add(request.user)
            
            return HttpResponseRedirect('/portal/')
            
    else:
        form = GroupForm()
        
    return render(request, 'portal/creategroup.html', {'form': form})
    
@login_required
def join_group_page(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            gname = form.cleaned_data['name']
            gpassword = form.cleaned_data['password']
            
            try:
                g = Group.objects.get(name=gname, password=gpassword)
                if g:
                    g.member_list.add(request.user)
                    return HttpResponseRedirect('/portal/')
            except Group.DoesNotExist:
                return render(request, 'portal/joingroup.html', 
                    {'form': form, 'error': 'Name/Password incorrect.'})
            
    else:
        form = GroupForm()
        
    return render(request, 'portal/joingroup.html', {'form': form})
    
@login_required
def group_page(request, id):
    g = Group.objects.get(pk=id)
    if not g:
        g = None
    return render(request, 'portal/group.html', {'group': g})
    
@login_required
def start_turn(request, id):
    g = Group.objects.get(pk=id)
    if g:
        if g.prev_turn:
            prev = g.prev_turn.owner
            if g.member_list.all()[-1] == prev:
                g.turn = g.member_list.all()[0]
            else:
                for i in range(g.member_list.all().len):
                    if g.member_list.all()[i] == prev:
                        g.turn = g.member_list.all()[i + 1]
                        break
        else:
            g.turn = g.member_list.all()[0]
        g.save()
    return HttpResponseRedirect('/portal/group/' + str(g.id)   )
            
                    