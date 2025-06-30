import os
import secrets

from django.contrib.auth import login
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import CustomUserCreationForm, PasswordEditForm, UserEditForm
from .models import CustomUser

from django.contrib.auth.models import Group


def email_verifications(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy("users:login"))


class LoginView(View):
    template_name = "users/login.html"


class LogoutView(View):
    template_name = "users/logout.html"
    next_page = reverse_lazy("messenger:main")


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("messenger:main")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False

        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}"

        # user.groups.add(Group.objects.get(name="Пользователи"))

        login(self.request, user)
        self._send_confrirm_email(user.email, url)
        return super().form_valid(form)


    def _send_confrirm_email(self, email, url):
        subject = "Подтверждение почты"
        message = f"Спасибо, что зарегистрировались на нашем сайте! Для подтверждения почты перейдите по ссылке: {url}"
        send_mail(subject, message, os.getenv("EMAIL_HOST_USER"), [email])


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = UserEditForm
    success_url = reverse_lazy("messenger:main")


class UserUpdatePasswordView(UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = PasswordEditForm
    success_url = reverse_lazy("messenger:main")
