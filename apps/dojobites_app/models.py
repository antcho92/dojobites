from __future__ import unicode_literals
from ..login_reg_app.models import User
from django.db import models

class RestaurantManager(models.Manager):
    def validate_restaurant(self, input):
        errors = []
        name = input['name']
        desc = input['description']
        if not name or name.isspace():
            errors.append('Please enter the name!')
        if not desc or desc.isspace():
            errors.append('Please enter the description.')
        if errors:
            return (False, errors)
        Restaurant.objects.create(name=name, description=desc, cuisine=input['cuisine'], takeout=input['takeout'], location='location')
        return (True, "Restaurant Added!")

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cuisine = models.CharField(max_length=255)
    takeout = models.BooleanField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RestaurantManager()

class Date(models.Model):
    date = models.DateTimeField()
    users = models.ManyToManyField(User, related_name='dates')
    restaurants = models.ManyToManyField(Restaurant, related_name='dates')

class CommentManager(models.Manager):
    def validate_comment(self, input, user_id):
        errors = []
        users = user_id
        content = input['content']
        if not content or content.isspace():
            errors.append('Please input a valid comment! (Only whitespace is not valid...)')
        if errors:
            return (False, errors)
        Comment.objects.create(content=content, date=1, user=user_id)
        return (True, "Comment added!")


class Comment(models.Model):
    content = models.TextField(max_length=2000)
    date = models.ForeignKey(Date)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()
