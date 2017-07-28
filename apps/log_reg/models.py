
from __future__ import unicode_literals
from django.db import models
import bcrypt, re, datetime
from django.contrib import messages
from django.db.models import Count

def function():
    pass

class UserManager(models.Manager):
    def validate(self, request):
        post_data = request.POST
        data_is_good = True
        #check names for emptyness see more in week 6 no. 2 -- move validation to models
        if len(post_data['first_name']) < 2:
            messages.error(request, "First Name must be at least two characters long")
            data_is_good=False
        if re.match('^[A-Za-z]*$', post_data['first_name']) is None:
            messages.error(request, "First Name must contain valid characters")
            data_is_good=False            
        if len(post_data['last_name']) < 2:
            messages.error(request, "Last Name must be at least two characters long")
            data_is_good=False
        if  re.match('^[A-Za-z]*$', post_data['last_name']) is None:
            messages.error(request, "Last Name must contain valid characters")
            data_is_good=False        
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', post_data['email']) is None or len(post_data['email']) < 1:
            messages.error(request, "Valid email format required")
            data_is_good=False
        if len(post_data['password']) < 8 or len(post_data['confirm_password']) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            data_is_good=False
        elif post_data['password'] != post_data['confirm_password']:
            messages.error(request, "Passwords do not match")
            data_is_good=False       
        elif self.filter(email=post_data['email']).exists():
            messages.error(request, "Email address already in use")
            data_is_good=False         
        if data_is_good is True:
            messages.success(request, "Successful registration!")
            hashed = bcrypt.hashpw(post_data['password'].encode(encoding="utf-8", errors="strict"), bcrypt.gensalt())
            user = self.create(
                first_name = post_data['first_name'],
                last_name = post_data['last_name'],
                email = post_data['email'],
                password = hashed
            )
        return data_is_good, user

    def login(self, request):
        post_data = request.POST
        data_is_good = True
        user = User.objects.filter(email=post_data['email'])
        if user:
            hashed = User.objects.get(email=post_data['email']).password.encode(encoding="utf-8", errors="strict")
            password = post_data['password'].encode(encoding="utf-8", errors="strict")
            if bcrypt.checkpw(password, hashed) is True:
                messages.success(request, "Successful login!")
                data_is_good = True
            else:
                messages.error(request, "Invalid password")
                data_is_good = False
        else:
            messages.error(request, "Invalid email")
            data_is_good = False
        return data_is_good

class User(models.Model):
    email = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class SecretManager(models.Manager):
    def addSecret(self, request, user_id):
        post_data = request.POST
        Secret.objects.create(secret=post_data['secret'], user = User.objects.get(id = user_id))     
        return self

    def likeSecret(self, request, sid, user_id):
        post_data = request.POST
        user = User.objects.get(id=user_id)
        secret = Secret.objects.get(id=sid)
        secret.like.add(user)
        likes = Secret.objects.annotate(num_likes=Count('like'))
        return likes

class Secret(models.Model):
    secret = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='user', null=True)
    like = models.ManyToManyField(User, related_name='liked')
    objects = SecretManager()

