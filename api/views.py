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
        

# Get, Edit, Delete a Gallery using the pk
class GalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Gallery.objects.for_user(self.request.user)
        else:
            return self.request.user.galleries

    def perform_destroy(self, instance):
        gallery = instance
        gallery.photos.clear()
        instance.delete()


# Photo Views

# Class to restrict file uploads to just images uploads
class ImageUploadParser(FileUploadParser):
    media_type = "image/*"


# Add Image File to Photo in Gallery and Delete Photo from Gallery using the pks
class GalleryPhotoUploadView(APIView):
    parser_classes = (ImageUploadParser, )

    def post(self, request, gallery_pk):
        gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']

        try:
            img = Image.open(file)
            img.verify()
        except:
            raise ParseError("Unsupported image type")
        
        photo = Photo(photo_by=request.user)
        photo.photo.save(file.name, file, save=True)
        serializer = PhotoSerializer(instance=photo, data=request.data)
        if serializer.is_valid():
            newphoto = serializer.save()
            newphoto.gallery.add(gallery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GalleryPhotoDeleteView(APIView):
    def delete(self, request, gallery_pk, photo_pk):
        gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)
        photo = get_object_or_404(request.user.photos, pk=photo_pk)
        gallery.photos.remove(photo)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# List Photo
class PhotoListView(generics.ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.for_user(self.request.user)


# Add Image File to Photo and Delete Photo using the pk
class PhotoUploadView(APIView):
    parser_classes = (ImageUploadParser, )

    # PUT image file in photo using the pk
    def post(self, request, photo_pk):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']

        try:
            img = Image.open(file)
            img.verify()
        except:
            raise ParseError("Unsupported image type")

        photo = Photo(photo_by=request.user)
        photo.photo.save(file.name, file, save=True)
        return Response(status=status.HTTP_200_OK)


# Get, Edit, Delete a Photo using the pk
class PhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Photo.objects.for_user(self.request.user)
        else:
            return self.request.user.photos
