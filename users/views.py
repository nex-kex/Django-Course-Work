import os

from django.views import View
from .forms import CustomUserCreationForm, UserEditForm, PasswordEditForm


from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.urls import reverse_lazy

from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import FormView

from .models import CustomUser


class LoginView(View):
    template_name = "users/login.html"


class LogoutView(View):
    template_name = "users/logout.html"
    next_page = reverse_lazy("messenger:main_page")

class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("messenger:main_page")

    # def form_valid(self, form):
    #     try:
    #         user = form.save()
    #         user.groups.add(Group.objects.get(name="Пользователи"))
    #         login(self.request, user)
    #         self.send_confrirm_email(user.email)
    #         return super().form_valid(form)
    #
    #     except IntegrityError:
    #         form.add_error("email", "Пользователь с таким email уже существует")
    #         return self.form_invalid(form)

    def send_confrirm_email(self, email):
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        recipient_list = [email]
        send_mail(subject, message, os.getenv("EMAIL_HOST_USER"), recipient_list)


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = UserEditForm
    success_url = reverse_lazy("messenger:main_page")


class UserUpdatePasswordView(UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = PasswordEditForm
    success_url = reverse_lazy("messenger:main_page")
