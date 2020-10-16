from rest_framework import serializers
from photogallery.models import Gallery, Photo, Comment
from users.models import User

# Nested Serializers
class NestedCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="comment_by.username", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "username",
            "body"
        ]

# Main Serializers
class PhotoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="photo_by.username", read_only=True)
    photo_thumb = serializers.ImageField(required=False)
    photo_large = serializers.ImageField(required=False)
    comments = NestedCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = [
            "id",
            "username",
            "photo",
            "photo_thumb",
            "photo_large",
            "camera",
            "public_photo",
            "comments"    
        ]

class GallerySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="gallery_of.all", read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Gallery
        fields = [
            "id",
            "username",
            "title",
            "public_gallery",
            "photos"
        ]