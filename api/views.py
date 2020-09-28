# Imports 
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from PIL import Image
from django.shortcuts import get_object_or_404

# Local File Imports
from .serializers import GallerySerializer, PhotoSerializer, NestedCommentSerializer
from photogallery.models import Gallery, Photo, Comment

# Views

# Gallery Views

class GalleryListCreateView(generics.ListCreateAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return Gallery.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        gallery = serializer.save()
        gallery.gallery_of.add(self.request.user)
        

# Get a Gallery
class GalleryDetailView(generics.RetrieveAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return Gallery.objects.for_user(self.request.user)

# Update a Gallery using the pk
class GalleryUpdateView(generics.UpdateAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return self.request.user.gallery_users

# Delete a Gallery
class GalleryDeleteView(generics.DestroyAPIView):
    serializer_class = GallerySerializer

    def perform_destroy(self, instance):
        instance.clear()
        instance.delete()

# Photo Views

# Add Photo to a Gallery
class GalleryPhotoCreateView(APIView):
    def post(self, request, gallery_pk):
        serializer = PhotoSerializer(data=request.data)
        gallery = get_object_or_404(request.user.gallery_users, pk=gallery_pk)
        if serializer.is_valid():
            photo = serializer.save(photo_by=request.user)
            gallery.photos.add(photo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Class to restrict file uploads to just images uploads
class ImageUploadParser(FileUploadParser):
    media_type = "image/*"


# Add Image File to Photo in Gallery and Delete Photo from Gallery using the pks
class GalleryPhotoUploadDeleteView(APIView):
    parser_classes = (ImageUploadParser, )

    # PUT image file in photo using the pk 
    def put(self, request, gallery_pk, photo_pk):
        gallery = get_object_or_404(request.user.gallery_users, pk=gallery_pk)
        photo = get_object_or_404(request.user.user_photos, pk=photo_pk)
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']

        try:
            img = Image.open(file)
            img.verify()
        except:
            raise ParseError("Unsupported image type")
        
        photo.photo.save(file.name, file, save=True)
        return Response(status=status.HTTP_200_OK)
    
    # DELETE the photo using the pk, after removing it from the Gallery
    def delete(self, request, gallery_pk, photo_pk):
        gallery = get_object_or_404(request.user.gallery_users, pk=gallery_pk)
        photo = get_object_or_404(request.user.user_photos, pk=photo_pk)
        gallery.photos.remove(photo)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Add or List Photo
class PhotoListCreateView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(photo_by=self.request.user)

# Add Image File to Photo and Delete Photo using the pk
class PhotoUploadDeleteView(APIView):
    parser_classes = (ImageUploadParser, )

    # PUT image file in photo using the pk
    def put(self, request, photo_pk):
        photo = get_object_or_404(request.user.user_photos, pk=photo_pk)
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']

        try:
            img = Image.open(file)
            img.verify()
        except:
            raise ParseError("Unsupported image type")

        photo.photo.save(file.name, file, save=True)
        return Response(status=status.HTTP_200_OK)

    # DELETE the photo using the pk
    def delete(self, request, photo_pk):
        photo = get_object_or_404(request.user.user_photos, pk=photo_pk)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Get a Photo using the pk
class PhotoDetailView(generics.RetrieveAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.for_user(self.request.user)

# Update a Photo using the pk
class PhotoUpdateView(generics.UpdateAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return self.request.user.user_photos

