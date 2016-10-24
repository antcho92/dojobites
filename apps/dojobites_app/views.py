from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..login_reg_app.models import User
from .models import *


def index(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    context = {
        "dates" : Date.objects.all()
    }

    return render(request, 'dojobites_app/index.html', context)

def join(request, restaurant_id):


    return redirect(reverse('bites:index'))

def unjoin(request, restaurant_id):

    return redirect(reverse('bites:index'))

def comment(request):
    if request.method=='POST':
        print request.POST
    return redirect(reverse('bites:index'))

def new(request):
    return render(request, 'dojobites_app/new.html')

def create(request):
    if request.method == "POST":
        Restaurant.objects.create(name=request.POST['name'], description=request.POST['description'],cuisine=request.POST['cuisine'],takeout=request.POST['takeout'],location='location')
    restaurants = Restaurant.objects.all()
    print "*"*70
    print "Restaurants:", restaurants.values()
    print "*"*70
    return redirect(reverse('bites:index'))
