import os
import secrets

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, ListView

from messenger.mixins import ManagerMixin
from .forms import CustomUserCreationForm, PasswordEditForm, UserEditForm
from .models import CustomUser


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
    success_url = reverse_lazy("users:email_notification")

    def form_valid(self, form):
        try:
            user = form.save()
            user.is_active = False

            token = secrets.token_hex(16)
            user.token = token
            user.save()

            host = self.request.get_host()
            url = f"http://{host}/users/email_confirm/{token}"

            user.groups.add(Group.objects.get(name="Пользователи"))
            login(self.request, user)

            self._send_confrirm_email(user.email, url)
            return super().form_valid(form)

        except IntegrityError:
            form.add_error("email", "Пользователь с таким email уже существует")
            return self.form_invalid(form)

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


class UserChangePassword(UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = PasswordEditForm
    success_url = reverse_lazy("messenger:main")

    def get_object(self, queryset=None):
        # Если есть токен в URL - восстановления пароля
        if "token" in self.kwargs:
            user = get_object_or_404(CustomUser, pk=self.kwargs["pk"], reset_password_token=self.kwargs["token"])
            return user
        return super().get_object(queryset)


    def form_valid(self, form):
        if "token" in self.kwargs:
            user = form.instance
            user.reset_password_token = None
            user.save()
        return super().form_valid(form)


class EmailNotification(TemplateView):
    template_name = "users/email_notification.html"


class UserForgotPassword(View):
    template_name = "users/forgotten_password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return redirect("users:register")

        token = secrets.token_hex(16)
        user.reset_password_token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/{user.pk}/reset_password/{token}"

        self._send_reset_password_email(user.email, url)

        return redirect("users:email_notification")

    def _send_reset_password_email(self, email, url):
        subject = "Восстановление пароля"
        message = f"Для восстановления пароля перейдите по ссылке: {url}"
        send_mail(subject, message, os.getenv("EMAIL_HOST_USER"), [email])


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.groups.filter(name="Менеджеры").exists()):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
