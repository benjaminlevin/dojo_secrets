from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Secret, function
from django.db.models import Count

def index(request):
    #context only for reviewing all registered users
    context = {
        "user" : User.objects.all()
    }
    return render(request, "log_reg/index.html", context)

def register(request):
    if request.method == 'POST':
        user = User.objects.validate(request)
        print 'check this yooooo'
        print user[0]
        if user[0] is False:
            print 'no go'
            return redirect('/')
        else:
            print user[1].id
            request.session['id'] = user[1].id
            request.session['name'] = user[1].first_name            
            return redirect('/secrets')
    print user[1].last_name
    return redirect("/")

def login(request):
    if request.method == 'POST':
        if User.objects.login(request) is True:
            user = User.objects.get(email=request.POST['email'])
            request.session['id'] = user.id
            request.session['name'] = user.first_name
            return redirect('/secrets')
        else:
            return redirect('/')

    else:
        return redirect('/')

def secrets(request):
    if request.session['id'] != None:
        context = {
            "user" : User.objects.filter(id=request.session['id']),
            "secret" : Secret.objects.annotate(num_likes=Count('like')).order_by('-created_at')[:5],
            "current_user" : User.objects.get(id=request.session['id']),
        }
        return render(request, "log_reg/secrets.html", context)
    else:
        return redirect('/')      

def popular(request):
    if request.session['name'] != None:
        context = {
            "user" : User.objects.filter(id=request.session['id']),
            "secret" : Secret.objects.annotate(num_likes=Count('like')).order_by('-num_likes'),
            "current_user" : User.objects.get(id=request.session['id']),
        }
        return render(request, "log_reg/popular.html", context)
    else:
        return redirect('/')      

def post(request):
    if request.method == "POST":
        Secret.objects.addSecret(request, request.session['id'])
        return redirect('/secrets')

def like(request):
    if request.method == "POST":
        Secret.objects.likeSecret(request, request.POST['sid'], request.session['id'])
        return redirect('/secrets')

def delete(request):
    secret = Secret.objects.get(id=request.POST['sid'])
    secret.delete()
    return redirect('/secrets')

def logout(request):
    request.session['id'] = None
    request.session['name'] = None
    return redirect('/')

#for clearing entire DB
def deletea(request):
    secret = Secret.objects.all()
    user = User.objects.all()
    secret.delete()        
    user.delete()
    return redirect('/')