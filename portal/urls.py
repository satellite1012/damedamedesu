from django.conf.urls import url, include
from portal.views import *

urlpatterns = [

    url(r'^$', portal_main_page),
    url(r'^mysongs/$', my_songs_page),
    url(r'^mysongs/addsong/$', add_song_page),
    url(r'^mysongs/remove/(?P<id>[0-9]*)$', remove_song),

]
