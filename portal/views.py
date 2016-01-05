from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from portal.models import Song, Group, Turn
from portal.forms import AddSongForm, SongForm, GroupForm, RatingForm

@login_required
def portal_main_page(request):
    """
    If users authenticated, direct them to main page. Otherwise take
    them to login page.
    """    
    g = request.user.group_set.all()
    
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
    nsongs = songs.filter(turn_time__isnull=True).order_by('time_added').reverse() #having turn time means gifted already
    osongs = songs.filter(turn_time__isnull=False).order_by('turn_time').reverse()[:10]
    return render(request, 'portal/mysongs.html',
        {'nsongs': nsongs, 'osongs': osongs},
        context_instance=RequestContext(request))
    
@login_required
def add_song_page(request):
    glist = request.user.group_set.all()
    mlist = User.objects.none()
    for g in glist:
        mlist = mlist | g.member_list.all().exclude(pk=request.user.pk)
    if request.method == 'POST':
        form = AddSongForm(request.POST, mlist=mlist)
        if form.is_valid():
            fname = form.cleaned_data['name']
            furl = form.cleaned_data['url']
            fsug = form.cleaned_data['suggested_members']
            
            existing = Song.objects.all().filter(recommender=request.user)
            if existing.count() >= 600:
                oldest = existing.filter(turn_time__isnull=False).order_by('turn_time')[0]
                oldest.delete()
            
            s = Song.objects.create(name=fname, url=furl,
                recommender=request.user)
            for m in fsug:
                s.suggested_members.add(m)
            s.save()
            
            return HttpResponseRedirect('/portal/mysongs/')
            
    else:
        form = AddSongForm(mlist=mlist)
        
    return render(request, 'portal/addsong.html', {'form': form})
    
@login_required
def edit_song_page(request, sid):
    try:
        # first check that user actually suggested this song
        s = Song.objects.get(pk=sid)
        if s.recommender != request.user:
            return HttpResponseRedirect('/portal/mysongs/')
    except Song.DoesNotExist:
        return HttpResponseRedirect('/portal/mysongs/')

    glist = request.user.group_set.all()
    mlist = User.objects.none()
    for g in glist:
        mlist = mlist | g.member_list.all().exclude(pk=request.user.pk)
    if request.method == 'POST':
        form = AddSongForm(request.POST, mlist=mlist)
        if form.is_valid():
            fname = form.cleaned_data['name']
            furl = form.cleaned_data['url']
            fsug = form.cleaned_data['suggested_members']
            
            s.name = fname
            s.url = furl
            s.suggested_members.clear()
            for m in fsug:
                s.suggested_members.add(m)
            s.save()
            
            return HttpResponseRedirect('/portal/mysongs/')
            
    else:
        data = {'name': s.name, 'url': s.url}
        if s.suggested_members.all().count() > 0:
            data['suggested_members'] = s.suggested_members.all()
        form = AddSongForm(mlist=mlist, initial=data)
        
    return render(request, 'portal/editsong.html', 
        {'form': form, 'sid': sid})
    
@login_required
def remove_song(request, sid):
    try:
        s = Song.objects.get(pk=sid)
        if s.recommender == request.user: 
            s.delete() 
    except Song.DoesNotExist:
        return HttpResponseRedirect('/portal/mysongs/')
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
                    return HttpResponseRedirect('/portal')
            except Group.DoesNotExist:
                return render(request, 'portal/joingroup.html', 
                    {'form': form, 'error': 'Name/Password incorrect.'})
    else:
        form = GroupForm()
        
    return render(request, 'portal/joingroup.html', {'form': form})
    
@login_required
def leave_group(request, gid):
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]    
    g.member_list.remove(request.user)
    return HttpResponseRedirect('/portal')    
    
@login_required
def group_page(request, gid):
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]
        
    s = Song.objects.all().filter(recommender=request.user,
        turn_time__isnull=True)
    if g.turn:
        s = s.filter(suggested_members=g.turn)
        try:
            gifted = g.prev_turn.song_list.all().get(recommender=request.user)
        except:
            gifted = None
            
        try: #if there's even one song in list with no rating, not done rating yet
            rated = g.prev_turn.song_list.all().exclude(rater__isnull=True)
        except:
            rated = None
    else:
        rated = None
        gifted = None
        
    return render(request, 'portal/group.html',
        {'group': g, 'nsongs': s, 'gifted': gifted, 'rated': rated})
    
@login_required
def gift_page(request, gid):
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]
        
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
                return HttpResponseRedirect('/portal/group/' + str(gid))
            except Group.DoesNotExist:
                return HttpResponseRedirect('/portal')
    else:
        form = SongForm()
        
    return render(request, 'portal/giftsong.html', 
        {'form': form, 'group': gid})

@login_required
def gift_song(request, gid, sid):
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]
    
    try:
        s = Song.objects.get(pk=sid)
        if s.recommender != request.user: # song doesn't belong to user
            return HttpResponseRedirect('/portal/group/' + str(gid))
    except Song.DoesNotExist:
        return HttpResponseRedirect('/portal/group/' + str(gid))
    
    s.turn_time = datetime.now()
    s.save()
    g.prev_turn.song_list.add(s)
    g.save()
    return HttpResponseRedirect('/portal/group/' + str(gid))
            
@login_required
def rate_song(request, gid, sid):
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]
    
    try:
        s = Song.objects.get(pk=sid)
        if s not in g.prev_turn.song_list.all(): # song wasn't gifted
            return HttpResponseRedirect('/portal/group/' + str(gid))
    except Song.DoesNotExist:
        return HttpResponseRedirect('/portal/group/' + str(gid))

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
                if s in g.prev_turn.song_list.all():
                    s.rater = request.user
                    if srating:
                        s.rating = srating
                    if srank:
                        s.rank = srank
                    if scomment:
                        s.comment = scomment
                    s.save()
                    return HttpResponseRedirect('/portal/group/' + str(gid))
            except Group.DoesNotExist or Song.DoesNotExist:
                return HttpResponseRedirect('/portal/group/' + str(gid))
    else:
        try:
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
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]
        
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
    return HttpResponseRedirect('/portal/group/' + str(gid))
            
@login_required
def end_turn(request, gid):
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]
            
    g.turn = None
    g.save()
    return HttpResponseRedirect('/portal/group/' + str(gid))
    
@login_required
def already_heard(request, gid, sid):
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]
    
    try:
        s = Song.objects.get(pk=sid)
        if s not in g.prev_turn.song_list.all(): # song wasn't gifted
            return HttpResponseRedirect('/portal/group/' + str(gid))
    except Song.DoesNotExist:
        return HttpResponseRedirect('/portal/group/' + str(gid))
    
    if g.turn == request.user and s in g.prev_turn.song_list.all():
        s.comment = 'Heard already'
        s.rater = request.user
        s.save()
        g.prev_turn.song_list.remove(s)
        g.save()
        
    return HttpResponseRedirect('/portal/group/' + str(gid))

@login_required
def auto_gift(request, gid):
    gg = Group.objects.filter(pk=gid, member_list=request.user)
    if gg.count() == 0:
        return HttpResponseRedirect('/portal') # not part of group
    g = gg[0]
    
    if g.turn == request.user:
        slist = g.prev_turn.song_list.all()
        for m in g.member_list.all():
            if m == request.user:
                continue
            if g.prev_turn.song_list.all().filter(recommender=m).count() == 0:
                sl = m.song_list.all().filter(suggested_members=request.user, turn_time__isnull=True)
                if sl.count() == 0:
                    continue
                s = sl.order_by('time_added')[0]
                s.turn_time = datetime.now()
                s.save()
                g.prev_turn.song_list.add(s)
                g.save()
    
    return HttpResponseRedirect('/portal/group/' + str(gid))
                
@login_required
def gift_history(request, uid):
    if not uid:
        uid = request.user.pk
    try:
        u = User.objects.all().get(pk=uid)
    except User.DoesNotExist:
        return HttpResponseRedirect('/portal')
    
    songs = Song.objects.all().filter(recommender=u,
        turn_time__isnull=False)
        
    return render(request, 'portal/gifthistory.html',
        {'songs': songs, 'name': u.username},
        context_instance=RequestContext(request))

@login_required
def rate_history(request, uid):
    if not uid:
        uid = request.user.pk
    try:
        u = User.objects.all().get(pk=uid)
    except User.DoesNotExist:
        return HttpResponseRedirect('/portal')

    songs = Song.objects.all().filter(rater=u)
    
    return render(request, 'portal/ratehistory.html',
        {'songs': songs, 'name': u.username},
        context_instance=RequestContext(request))
    
    