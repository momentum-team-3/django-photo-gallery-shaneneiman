"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# django imports
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

# views imports
from photogallery import views 
from users import views as user_views
from api import views as api_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path("", views.index_randomlist, name="index"),
    path("search/", views.search, name="search"),
    # User URLS
    path("accounts/profile/", user_views.view_profile, name="profile"),
    # Photo URLS
    path("photo/add/", views.add_photo, name="add_photo"),
    path("photo/edit/<int:photo_pk>", views.edit_photo, name="edit_photo"),
    path("photo/delete/<int:photo_pk>", views.delete_photo, name="delete_photo"),
    path("photo/userphotos", views.user_photos_list, name="user_photos"),
    path("photo/view/<int:photo_pk>", views.view_photo, name="view_photo"),
    path("photo/comment/<int:photo_pk>", views.add_comment, name="add_comment"),
    path("photo/<int:photo_pk>/starred/",views.toggle_fav_photo, name="toggle_fav_photo"),
    # Gallery URLS
    path("gallery/add/", views.add_gallery, name="add_gallery"),
    path("gallery/addphoto/<int:gallery_pk>", views.add_photo_to_gallery, name="add_photo_to_gallery"),
    path("gallery/delete/<int:gallery_pk>", views.delete_gallery, name="delete_gallery"),
    path("gallery/deletegalleryandphotos/<int:gallery_pk>", views.delete_gallery_and_photos, name="delete_gallery_and_photos"),
    path("gallery/usergalleries", views.user_galleries_list, name="user_galleries"),
    path("gallery/view/<int:gallery_pk>", views.view_gallery, name="view_gallery"),
    path("gallery/edit/<int:gallery_pk>", views.edit_gallery, name="edit_gallery"),
    # API URLS 
    # Galleries
    path("api/galleries/", api_views.GalleryListCreateView.as_view()),
    path("api/galleries/<int:pk>", api_views.GalleryDetailView.as_view()),
    path("api/galleries/<int:gallery_pk>/addphoto/", api_views.GalleryPhotoUploadView.as_view()),
    path("api/galleries/<int:gallery_pk>/photos/<int:photo_pk>/delete", api_views.GalleryPhotoDeleteView.as_view()),
    # Photos
    path("api/photos/", api_views.PhotoListView.as_view()),
    path("api/photos/add/", api_views.PhotoUploadView.as_view()),
    path("api/photos/<int:pk>", api_views.PhotoDetailView.as_view()),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
