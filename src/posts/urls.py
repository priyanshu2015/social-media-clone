from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.UploadPostView.as_view(), name="upload-post")
]