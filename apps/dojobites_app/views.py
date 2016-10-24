from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse

def index(request):
    return render(request, 'dojobites_app/index.html')

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
