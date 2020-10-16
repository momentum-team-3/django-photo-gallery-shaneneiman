from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill

# Consider creating a custom user model from scratch as detailed at
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to="users/", null=True, blank=True)
    profile_photo_thumb = ImageSpecField(source="profile_photo", processors=[ResizeToFill(200,200)], format="JPEG", options={"quality": 80})
    bio = models.CharField(max_length=200, null=True, blank=True)