from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^join/(?P<restaurant_id>)$', views.vote, name='join'),
    url(r'^unjoin/(?P<restaurant_id>)$', views.unvote, name='unjoin'),
    url(r'^new$', views.new, name='new'),
    url(r'^create$', views.create, name='create'),

]
