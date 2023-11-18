from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.UploadPostView.as_view(), name="upload-post"),
    path("<slug:uuid>/", views.PostDetail.as_view(), name="post-detail"),
    path("<slug:uuid>/comments/", views.PostCommentView.as_view(), name="post-comment")
]