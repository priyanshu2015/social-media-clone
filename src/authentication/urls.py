from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate")
]