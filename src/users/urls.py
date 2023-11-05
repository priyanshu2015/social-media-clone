from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("profile/<slug:username>/", views.GetProfileView.as_view(), name="profile"),
    path("users/<slug:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("users/<slug:username>/unfollow/", views.UnfollowView.as_view(), name="unfollow"),
]