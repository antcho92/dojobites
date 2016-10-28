from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^join$', join, name='join'),
    url(r'^join/(?P<choice_id>\d+)$', join_choice, name='join_choice'),
    url(r'^random$', random, name='random'),
    url(r'^unjoin/(?P<choice_id>\d+)$', unjoin_choice, name='unjoin_choice'),
    url(r'^new$', new, name='new'),
    url(r'^create$', create, name='create'),
    url(r'^comment$', comment, name='comment'),
    url(r'^show/choice$', show_choice, name='show_choice'),
    url(r'^show/restaurant$', show_rest, name='show_rest'),
    url(r'^show/direction/(?P<restaurant_id>\d+)$', direction, name='direction'),
    url(r'^details/(?P<restaurant_id>\d+)$', details, name='details'),
    url(r'^calendar$', calendar, name='calendar'),
    url(r'^profile$', profile, name='profile')
]
