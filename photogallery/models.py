from django.db import models
from django.db.models import Q, Count
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from django.contrib.postgres.search import SearchVector
from users.models import User


class PhotoQuerySet(models.QuerySet):
    def count_interactions(self):
        photos = self.annotate(
            num_stars=Count("starred_by", distinct=True),
            num_comments=Count("comments", distinct=True),
        )
        return photos

    def interacted_with(self):
        photos = self.count_interactions().filter(
            Q(num_comments__gt=0) | Q(num_stars__gt=0)
        ).order_by("num_stars", "num_comments").reverse()
        return photos
    
    def public(self):
        photos = self.exclude(public_photo=False)
        return photos

    def search(self):
        photos = self.annotate(
            search=SearchVector("photo_by__username", "camera", "comments__body")
        )
        return photos

    def for_user(self, user):
        if user.is_authenticated:
            photos = self.filter(Q(public_photo=True) | Q(photo_by=user))
        else:
            photos = self.filter(public_photo=True)
        return photos


class Photo(models.Model):
    objects = PhotoQuerySet.as_manager()

    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    photo_thumb = ImageSpecField(source="photo", processors=[ResizeToFill(200,200)], format="JPEG", options={"quality": 80})
    photo_large = ImageSpecField(source="photo", processors=[ResizeToFit(600,600)], format="JPEG", options={"quality": 90})
    photo_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="photos", null=True, blank=True)
    photo_added_date = models.DateField(auto_now_add=True)
    camera = models.CharField(max_length=100, null=True, blank=True)
    is_user_favorite = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="favorites", null=True, blank=True)
    starred_by = models.ManyToManyField(to=User, related_name="starred_photos", blank=True)
    public_photo = models.BooleanField(default=True)


class GalleryQuerySet(models.QuerySet):
    def public(self):
        galleries = self.exclude(public_gallery=False)
        return galleries

    def search(self):
        galleries = self.annotate(
            search=SearchVector("title", "gallery_of__username", "photos__camera")
        )
        return galleries

    def for_user(self, user):
        if user.is_authenticated:
            galleries = self.filter(Q(public_gallery=True) | Q(gallery_of=user))
        else:
            galleries = self.filter(public_gallery=True)
        return galleries

class Gallery(models.Model):
    objects = GalleryQuerySet.as_manager()

    title = models.CharField(max_length=100, null=False, blank=False)
    photos = models.ManyToManyField(to=Photo, related_name="gallery", blank=True)
    gallery_of = models.ManyToManyField(to=User, related_name="galleries", blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    public_gallery = models.BooleanField(default=True)


class Comment(models.Model):
    comment_by = models.ForeignKey(to=User, on_delete=models.CASCADE ,related_name="comments", null=True, blank=True)
    comments = models.ForeignKey(to=Photo, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    body = models.TextField(null=False, blank=False)
    comment_date = models.DateTimeField(auto_now_add=True)