from django.conf.urls import patterns, url, include
from portal.views import *

urlpatterns = patterns('',

    (r'^$', portal_main_page),

)
