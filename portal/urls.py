from django.conf.urls import url, include
from portal.views import *

urlpatterns = [

    url(r'^$', portal_main_page),
    url(r'^mysongs/$', my_songs_page),

]
