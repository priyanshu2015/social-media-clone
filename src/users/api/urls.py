from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ProfileEditView

urlpatterns = [
    path("profile/", ProfileEditView.as_view(), name="profile-update"),
]