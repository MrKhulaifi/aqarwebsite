from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class AgencyManager(models.Manager):
    def new(self, user, **kwargs):
        name = kwargs.get("name")
        if name is None or len(name) < 10:
            raise ValidationError("Name should be longer than 10 charters")

        phone_number = kwargs.get("phone_number")
        if phone_number is not None and len(phone_number) < 8:
            raise ValidationError("Phone number should be 8 numbers")

        email = kwargs.get("email")
        if email is not None:
            email_validator = EmailValidator("Should have a valid email")
            email_validator(email)

        agency = self.create(**kwargs)
        # agency.add_member(user, is_admin= True)
        AgencyMember.objects.create(agency=agency, member=user, is_admin= True)
        
        return agency

class Agency(models.Model):
    name = models.CharField(max_length=100,blank=False)
    phone_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to="profile_picture", null=True)
    email = models.EmailField()
    address = models.TextField(max_length=200)
    verification = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name="verified")
    twitter = models.CharField(max_length=50)
    instagram = models.CharField(max_length=50)

    members = models.ManyToManyField(User, through='AgencyMember')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AgencyManager()

    def verified_by(self, user):
        self.verification = user
        self.save()

    def add_post(self, user, **kwargs):
        pass

    def add_member(self, user, is_admin= False):
        pass

class AgencyMember(models.Model):
    agency = models.ForeignKey(Agency, on_delete=CASCADE)
    member = models.ForeignKey(User, on_delete=CASCADE)

    is_admin = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Area(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    agency = models.ForeignKey(Agency, on_delete=CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=400, blank=False)
    picture = models.ImageField(upload_to="posts", null=True)
    area = models.ForeignKey(Area, on_delete=CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_comment(self, user, message):
        pass

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=CASCADE)
    message = models.TextField(max_length=400, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
