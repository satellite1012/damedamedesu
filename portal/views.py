from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from portal.models import Song, Group, Turn
from portal.forms import SongForm, GroupForm, RatingForm

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
    nsongs = songs.filter(turn_time__isnull=True) #having turn time means gifted already
    osongs = songs.filter(turn_time__isnull=False)
    return render(request, 'portal/mysongs.html',
        {'nsongs': nsongs, 'osongs': osongs},
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
def remove_song(request, sid):
    s = Song.objects.get(pk=sid)
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
def group_page(request, gid):
    try:
        g = Group.objects.get(pk=gid)
        s = Song.objects.all().filter(recommender=request.user,
            turn_time__isnull=True)
        if g.turn:
            try:
                gifted = g.prev_turn.song_list.all().get(recommender=request.user)
            except:
                gifted = None
        else:
            gifted = None
    except Group.DoesNotExist:
        return HttpResponseRedirect('/portal')
    return render(request, 'portal/group.html',
        {'group': g, 'nsongs': s, 'gifted': gifted})
    
@login_required
def gift_page(request, gid):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['name']
            furl = form.cleaned_data['url']
            
            #could potentially enforce song uniqueness here
            s = Song.objects.create(name=fname, url=furl,
                recommender=request.user, turn_time=datetime.now())
            try:
                g = Group.objects.get(pk=gid)
                g.prev_turn.song_list.add(s)
                g.save()
                return HttpResponseRedirect('/portal/group/' + str(g.id))
            except Group.DoesNotExist:
                return HttpResponseRedirect('/portal/group/' + str(g.id) + '/gift')
            
    else:
        form = SongForm()
        
    return render(request, 'portal/giftsong.html', 
        {'form': form, 'group': gid})

@login_required
def gift_song(request, gid, sid):
    g = Group.objects.get(pk=gid)
    s = Song.objects.get(pk=sid)
    s.turn_time = datetime.now()
    s.save()
    g.prev_turn.song_list.add(s)
    g.save()
    return HttpResponseRedirect('/portal/group/' + str(g.id))
    
@login_required
def rate_song(request, gid, sid):    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            srating = None
            srank = None
            scomment = None
            if 'rating' in form.cleaned_data:
                srating = form.cleaned_data['rating']
            if 'rank' in form.cleaned_data:
                srank = form.cleaned_data['rank']
            if 'comment' in form.cleaned_data:
                scomment = form.cleaned_data['comment']
        
            try:
                s = Song.objects.get(pk=sid)
                g = Group.objects.get(pk=gid)
                
                if s in g.prev_turn.song_list.all():
                    s.rater = request.user
                    if srating:
                        s.rating = srating
                    if srank:
                        s.rank = srank
                    if scomment:
                        s.comment = scomment
                    s.save()
                    return HttpResponseRedirect('/portal/group/' + str(g.id))
            except Group.DoesNotExist or Song.DoesNotExist:
                return HttpResponseRedirect('/portal/group/' + str(g.id))
            
    else:
        try:
            s = Song.objects.get(pk=sid)
            data = {}
            if s.rating:
                data['rating'] = s.rating
            if s.rank:
                data['ranking'] = s.rank
            if s.comment:
                data['comment'] = s.comment
            form = RatingForm(initial=data)
        except Song.DoesNotExist:
            return HttpResponseRedirect('/portal/group/' + str(gid))
        
    return render(request, 'portal/ratesong.html', 
        {'form': form, 'song': s, 'gid': gid})
        
@login_required
def start_turn(request, gid):
    g = Group.objects.get(pk=gid)
    mlist = g.member_list.order_by('username').all()
    if g.prev_turn:
        prev = g.prev_turn.owner
        if mlist.reverse()[0] == prev:
            g.turn = mlist[0]
        else:
            for i in range(0, mlist.count() - 1):
                if mlist[i] == prev:
                    g.turn = mlist[i + 1]
                    break
        g.prev_turn.delete()
    else:
        g.turn = mlist[0]

    g.prev_turn = Turn.objects.create(owner=g.turn)
    g.prev_turn.save()  
    g.save()
    return HttpResponseRedirect('/portal/group/' + str(g.id))
            
@login_required
def end_turn(request, gid):
    g = Group.objects.get(pk=gid)
    g.turn = None
    g.save()
    return HttpResponseRedirect('/portal/group/' + str(g.id))
    