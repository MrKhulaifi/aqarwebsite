from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Agency(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to="profile_picture", null=True)
    email = models.EmailField()
    address = models.TextField(max_length=200)
    verification = models.BooleanField(default=False)
    twitter = models.CharField(max_length=50)
    instagram = models.CharField(max_length=50)

    members = models.ManyToManyField(User, through='AgencyMember')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AgencyMember(models.Model):
    agency = models.ForeignKey(Agency, on_delete=CASCADE)
    member = models.ForeignKey(User, on_delete=CASCADE)

    is_admin = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Area(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    agency = models.ForeignKey(Agency, on_delete=CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=400, blank=False)
    picture = models.ImageField(upload_to="posts", null=True)
    area = models.ForeignKey(Area, on_delete=CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    message = models.TextField(max_length=400, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
