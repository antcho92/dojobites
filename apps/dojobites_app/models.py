from __future__ import unicode_literals
from ..login_reg_app.models import User
from django.db import models



class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cuisine = models.CharField(max_length=255)
    takeout = models.BooleanField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Date(models.Model):
    date = models.DateTimeField()
    users = models.ManyToManyField(User, related_name='dates')
    restaurants = models.ManyToManyField(Restaurant, related_name='dates')
