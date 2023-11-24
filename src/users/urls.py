from django.contrib import admin
from django.urls import path, include
from . import views
from posts.views import ListPosts

urlpatterns = [
    path("users/<slug:username>/", views.GetProfileView.as_view(), name="profile"),
    path("users/<slug:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("users/<slug:username>/unfollow/", views.UnfollowView.as_view(), name="unfollow"),
    path("users/<slug:username>/posts/", ListPosts.as_view(), name="list-user-posts")
]