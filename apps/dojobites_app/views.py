from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..login_reg_app.models import User
from .models import Restaurant, Date


def index(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    context = {
        "dates" : Date.objects.all()
    }

    return render(request, 'dojobites_app/index.html', context)

def vote(request, restaurant_id):


    return redirect(reverse('bites:index'))

def unvote (request, restaurant_id):

    return redirect(reverse('bites:index'))
