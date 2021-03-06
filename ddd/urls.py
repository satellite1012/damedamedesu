
from django.conf.urls import *
from ddd.views import *
import django.contrib.auth.views
import django.views.static

urlpatterns = [
    url(r'^$', main_page),

    url(r'^register/$', register),
    url(r'^login/$', django.contrib.auth.views.login),
    url(r'^logout/$', logout_page),
    url(r'^data/$', data_page_games),
    url(r'^data/bygames/$', data_page_games),
    url(r'^data/byrate/$', data_page_rate),
    url(r'^data/pastmonth/$', data_page_month),

    url(r'^portal/', include('portal.urls')),

    url(r'^static/(?P<path>.*)$', django.views.static.serve,
        {'document_root': 'static'}),
]

