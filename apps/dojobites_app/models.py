from __future__ import unicode_literals
from ..login_reg_app.models import User
from django.db import models
from datetime import datetime

class RestaurantManager(models.Manager):
    def validate_restaurant(self, input):
        errors = []
        name = input['name']
        desc = input['description']
        if not name or name.isspace():
            errors.append('Please enter the name!')
        elif self.filter(name__iexact=name).exists():
            errors.append('Restaurant already existed!')
        if not desc or desc.isspace():
            errors.append('Please enter the description.')
        if errors:
            return (False, errors)
        self.create(name=name, description=desc, cuisine=input['cuisine'], takeout=input['takeout'], location='location')
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
    def __str__(self):
        return self.name
    # def count(self, choices):
    #     return len(choices.filter(restaurant=self))
    # def attendees(self, choices, ):
    #     pass

class CommentManager(models.Manager):
    def validate_comment(self, input, user_id):
        errors = []
        user = User.objects.get(id=user_id)
        date = Date.objects.create(date=datetime.now())
        content = input['content']
        if not content or content.isspace():
            errors.append('Please input a valid comment! (Only whitespace is not valid...)')
        if errors:
            return (False, errors)
        Comment.objects.create(content=content, date=date, user=user)
        return (True, "Comment added!")

class ChoiceManager(models.Manager):
    def addChoice(self, input, user):
        errors = []
        date = input['date']
        rest_id = input['restaurant']
        if not rest_id or not date:
            errors.append("Must choose and date and restaurant")
        if rest_id and date:
            today = datetime.now().strftime('%Y-%m-%d')
            if date <= today:
                errors.append("Meal date must be in the future")
        if errors:
            return (False, errors)
        else:
            r = Restaurant.objects.get(id=rest_id)
            if Choice.objects.filter(date=date, users=user).exists():
                errors.append("You have already made your choice today!")
                return (False, errors)
            choice = Choice.objects.filter(date=date, restaurant=r)
            if not choice.exists():
                choice = Choice.objects.create(date=date, restaurant=r)
                choice.users.add(user)
            else:
                choice[0].users.add(user)
            return (True, "You made a choice!")

class Choice(models.Model):
    date = models.DateField()
    users = models.ManyToManyField(User, related_name='choices')
    restaurant = models.ForeignKey(Restaurant)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.restaurant + self.users.all
    objects = ChoiceManager()

class Comment(models.Model):
    content = models.TextField(max_length=2000)
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
    # def __str__(self):
    #     return self.content
