from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote/(?P<restaurant_id>)$', views.vote, name='vote'),
    url(r'^unvote/(?P<restaurant_id>)$', views.unvote, name='unvote'),
    url(r'^new$', views.new, name='new'),
    url(r'^create$', views.create, name='create'),

]
