#Django Imports 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse


#Project File Imports
from .models import Photo, Gallery, Comment
from .forms import PhotoForm, GalleryForm, CommentForm


# Views
@login_required
def add_comment(request, photo_pk):
    if request.method == "GET":
        form = CommentForm()
    else:
        photo = get_object_or_404(Photo.objects.for_user(request.user), pk=photo_pk)
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.comment_by = request.user
            comment.comments = photo
            comment.save()
            return redirect(to="view_photo", photo_pk=photo_pk)
    return render(request, "photogallery/add_comment.html", {
        "form": form
    })


@login_required
def add_gallery(request):
    if request.method == "GET":
        form = GalleryForm()
    else:
        form = GalleryForm(request.POST, files=request.FILES)
        if form.is_valid:
            gallery = form.save()
            gallery.gallery_of.add(request.user)
            gallery.save()
            return redirect(to="view_gallery", gallery_pk=gallery.pk)
    return render(request, "photogallery/add_gallery.html", {
        "form": form
    })


@login_required
def add_photo(request):
    if request.method =="GET":
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, files=request.FILES)
        if form.is_valid:
            photo = form.save(commit=False)
            photo.photo_by = request.user
            photo.save()
            return redirect(to="user_photos")
    return render(request, "photogallery/add_photo.html", {
        "form": form
    })


@login_required
def add_photo_to_gallery(request, gallery_pk):
    if request.method == "GET":
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, files=request.FILES)
        gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)
        if form.is_valid:
            photo = form.save(commit=False)
            photo.photo_by = request.user
            photo.save()
            photo.gallery.add(gallery)
            photo.save()
            return redirect(to="view_gallery", gallery_pk=gallery_pk)
    return render(request, "photogallery/add_photo_to_gallery.html", {
        "form": form
    })



@login_required
def delete_gallery(request, gallery_pk):
    gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)
    if request.method == "POST":
        gallery.clear()
        gallery.delete()
        return redirect ("user_galleries")
    return render (request, "photogallery/delete_gallery.html", {
        "gallery": gallery
    })


@login_required
def delete_gallery_and_photos(request, gallery_pk):
    gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)
    user = request.user
    if request.method == "POST":
        for photo in gallery.photos:
            gallery.remove(photo)
            photo.delete()
            return gallery
        gallery.delete()
        return redirect ("user_galleries")
    return render (request, "photogallery/delete_gallery_and_photos.html", {
        "gallery": gallery
    })


@login_required
def delete_photo(request, photo_pk):
    photo = get_object_or_404(request.user.photos, pk=photo_pk)
    if request.method == "POST":
        photo.delete()
        return redirect ("user_photos")
    return render (request, "photogallery/delete_photo.html", {
        "photo": photo
    })


@login_required
def edit_gallery(request, gallery_pk):
    gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)
    photos = gallery.photos.all()
    if request.method == "GET":
        form = GalleryForm(instance=gallery)
    else:
        form = GalleryForm(request.POST, instance=gallery)
        if form.is_valid():
            form.save()
            return redirect("view_gallery", gallery_pk=gallery.pk)
    return render(request, "photogallery/edit_gallery.html", {
        "gallery": gallery,
        "photos": photos,
        "form": form,
    })


@login_required
def edit_photo(request, photo_pk):
    photo = get_object_or_404(request.user.photos, pk=photo_pk)
    if request.method == "GET":
        form = PhotoForm(instance=photo)
    else:
        form = PhotoForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return redirect("view_photo", photo_pk=photo.pk)
    return render(request, "photogallery/edit_photo.html", {
        "photo": photo,
        "form": form
    })

def index_randomlist(request):
    photos = Photo.objects.public().interacted_with()[:4]
    all_photos = Photo.objects.public().order_by('?').all()[:8]
    return render(request, "photogallery/index.html", {
        "photos": photos,
        "all_photos": all_photos
    })

def search(request):
    query = request.GET.get("q")
    public_photos = Photo.objects.public()
    public_galleries = Gallery.objects.public()
    if query is not None:
        galleries = public_galleries.search().filter(search=query).distinct("pk")
        photos = public_photos.search().filter(search=query).distinct("pk")
    else:
        galleries = None
        photos = None
    return render(request, "photogallery/search.html", {
        "galleries": galleries,
        "photos": photos,
        "query": query or ""
    })


@login_required
@csrf_exempt
@require_POST
def toggle_fav_photo(request, photo_pk):
    photo = get_object_or_404(Photo.objects.for_user(request.user), pk=photo_pk)
    if photo in request.user.starred_photos.all():
        request.user.starred_photos.remove(photo)
        return JsonResponse({"starred_photo": False})
    else:
        request.user.starred_photos.add(photo)
        return JsonResponse({"starred_photo": True})


@login_required
def user_galleries_list(request):
    galleries = request.user.galleries.all()
    return render(request, "photogallery/user_galleries_list.html", {
        "galleries": galleries
    })


@login_required
def user_photos_list(request):
    photos = request.user.photos.all()
    return render(request, "photogallery/user_photos_list.html", {
        "photos": photos
    })


def view_gallery(request, gallery_pk):
    gallery = get_object_or_404(Gallery, pk=gallery_pk)
    photos = gallery.photos.all()
    user_list = list(gallery.gallery_of.all())    
    return render(request, "photogallery/view_gallery.html", {
        "gallery": gallery,
        "photos": photos,
        "PhotoForm": PhotoForm,
        "gallery_pk": gallery_pk,
        "user_list": user_list
    })


@login_required
def view_photo(request, photo_pk):
    photo = get_object_or_404(Photo.objects.for_user(request.user).count_interactions(), pk=photo_pk)
    comments = photo.comments.order_by("comment_date").reverse()
    starred_photo = False
    gallery = None
    if photo in request.user.starred_photos.all():
        starred_photo = True
    if photo.gallery.all() is not None:
        gallery = photo.gallery.first()
    if request.method == "GET":
        form = PhotoForm(instance=photo)
    else:
        form = PhotoForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return redirect("view_photo", photo_pk=photo.pk)
    return render(request, "photogallery/view_photo.html", {
        "photo": photo,
        "form": form,
        "comments": comments,
        "CommentForm": CommentForm,
        "photo_pk": photo_pk,
        "starred_photo": starred_photo,
        "gallery": gallery
    })