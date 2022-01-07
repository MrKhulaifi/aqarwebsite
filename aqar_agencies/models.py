from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, validate_image_file_extension


class AgencyManager(models.Manager):
    def new(self, user, **kwargs):
        name = kwargs.get("name")
        if not name:
            raise ValidationError("Please enter a name for the Agency.")
        name_min_validator = MinLengthValidator(10)
        name_min_validator(name)
        name_max_validator = MaxLengthValidator(100)
        name_max_validator(name)

        phone_number = kwargs.get("phone_number")
        if phone_number:
            if phone_number and not str(phone_number).isnumeric():
                raise ValidationError("Please enter a valid phone number")
            if phone_number is not None and len(phone_number) != 8:
                raise ValidationError("Phone number should be 8 numbers")

        profile_picture = kwargs.get("profile_picture")
        if profile_picture:
            validate_image_file_extension(profile_picture)

        email = kwargs.get("email")
        if email:
            email_validator = EmailValidator("Should have a valid email")
            email_validator(email)

        address = kwargs.get("address")
        if address:
            address_min_validator = MinLengthValidator(30)
            address_min_validator(address)
            address_max_validator = MaxLengthValidator(200)
            address_max_validator(address)

        agency = self.create(**kwargs)
        agency.add_member(user, is_admin=True)
        
        return agency


class Agency(models.Model):
    name = models.CharField(max_length=100,blank=False)
    phone_number = models.CharField(max_length=8, blank=True)
    profile_picture = models.ImageField(upload_to="profile_picture", null=True, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(max_length=200, blank=True)
    verification = models.ForeignKey(User, null=True, blank=True, on_delete=SET_NULL, related_name="verified")
    twitter = models.CharField(max_length=50, blank=True)
    instagram = models.CharField(max_length=50, blank=True)

    members = models.ManyToManyField(User, through='AgencyMember')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AgencyManager()

    class Meta:
        verbose_name_plural = "agencies"

    def clean(self, *args, **kwargs):
        # Do something
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def verified_by(self, user):
        if self.verification is not None:
            raise ValidationError("Agency has already been verified")
        self.verification = user
        self.save()

    def unverify(self):
        if self.verification is None:
            raise ValidationError("Agency is not verified")
        self.verification = None
        self.save()

    def add_post(self, **kwargs):
        Post.objects.new(self, **kwargs)

    def add_member(self, user, is_admin):
        AgencyMember.objects.create(agency=self, member=user, is_admin=is_admin)

    def __str__(self):
        return self.name


class AgencyMember(models.Model):
    agency = models.ForeignKey(Agency, on_delete=CASCADE)
    member = models.ForeignKey(User, on_delete=CASCADE)

    is_admin = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agency.name

    class Meta:
        verbose_name_plural = "agencies"


class AreaManager(models.Manager):
    def new(self, **kwargs):
        name = kwargs.get("name")
        if name is None:
            raise ValidationError("Please enter a name for the Area.")
        elif name in [area.name for area in self.all()]:
            raise ValidationError("The name already exists. Please enter another one.")
        name_min_validator = MinLengthValidator(2)
        name_min_validator(name)
        name_max_validator = MaxLengthValidator(50)
        name_max_validator(name)

        area = self.create(**kwargs)

        return area


class Area(models.Model):
    name = models.CharField(max_length=50)

    objects = AreaManager()

    def __str__(self):
        return f"{self.area}"


class PostManager(models.Manager):
    def new(self, **kwargs):
        title = kwargs.get("title")
        if title is None:
            raise ValidationError("Please enter a title for the post")
        title_max_validator = MaxLengthValidator(100)
        title_max_validator(title)

        body = kwargs.get("body")
        if body is None:
            raise ValidationError("Please enter text in the body")
        body_max_validator = MaxLengthValidator(400)
        body_max_validator(body)

        profile_picture = kwargs.get("picture")
        if profile_picture is not None:
            validate_image_file_extension(profile_picture)

        post = self.create(**kwargs)

        return post


class Post(models.Model):
    agency = models.ForeignKey(Agency, on_delete=CASCADE, related_name="posts")
    area = models.ForeignKey(Area, on_delete=CASCADE)
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField(max_length=400, blank=False)
    picture = models.ImageField(upload_to="posts", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()

    def add_comment(self, user, message):
        pass

    def __str__(self):
        title_abbreviation = self.title[:10]
        return f"{title_abbreviation}... posted on {self.created_at} by {self.agency}"


class CommentManager(models.Manager):
    def new(self, **kwargs):
        message = kwargs.get("message")
        if message is None:
            raise ValidationError("Please enter a message in the comment section")
        message_max_validator = MaxLengthValidator(400)
        message_max_validator(message)

        comment = self.create(**kwargs)

        return comment


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=CASCADE)
    message = models.TextField(max_length=400, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __str__(self):
        message_abbreviation = self.message[:10]
        return f"{message_abbreviation}... posted on {self.created_at} by {self.agency}"
