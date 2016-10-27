from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^join$', join, name='join'),
    url(r'^join/(?P<date>.+)/(?P<restaurant_id>\d+)$', join_ajax, name='join_ajax'),
    url(r'^unjoin/(?P<restaurant_id>\d+)$', unjoin, name='unjoin'),
    url(r'^new$', new, name='new'),
    url(r'^create$', create, name='create'),
    url(r'^comment$', comment, name='comment'),
    url(r'^show/choice$', show_choice, name='show_choice'),
    url(r'^show/restaurant$', show_rest, name='show_rest'),
    url(r'^details/(?P<restaurant_id>\d+)$', details, name='details'),
    url(r'^calendar$', calendar, name='calendar'),
    url(r'^profile$', profile, name='profile')
]
