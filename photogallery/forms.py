from django import forms
from .models import Photo, Gallery, Comment

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            "photo",
            "camera",
            "public_photo",
        ]


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = [
            "title",
            "public_gallery",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "body",
        ]