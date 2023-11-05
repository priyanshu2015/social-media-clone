from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('login/', views.LoginUserView.as_view(), name="login"),
    path('logout/', views.LogoutUserView.as_view(), name="logout"),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='authentication/password_change.html', success_url=reverse_lazy("password_change_done")), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="authentication/password_change_done.html"), name="password_change_done"),

    # forgot password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authentication/password_reset.html", success_url=reverse_lazy("password_reset_done"), email_template_name="authentication/forgot_password_email.html")),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="authentication/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_form.html", success_url=reverse_lazy("password_reset_complete")), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset_done.html"), name="password_reset_complete")
]