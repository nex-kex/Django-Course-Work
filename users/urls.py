from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig

from . import views

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="messenger:main"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("<int:pk>/update_password/", views.UserUpdatePasswordView.as_view(), name="user_update_password"),
    path("email_confirm/<str:token>/", views.email_verifications, name="email_confirm"),
    path("email_notification/", views.EmailNotification.as_view(), name="email_notification"),
    path("forgotten_password/", views.UserForgotPassword.as_view(), name="forgotten_password"),
    path("<int:pk>/reset_password/<str:token>/", views.UserChangePassword.as_view(), name="reset_password"),
]
