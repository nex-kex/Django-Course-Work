from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.management import call_command
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)

from . import forms
from .mixins import ManagerMixin
from .models import Client, Mailing, Message, Attempt


class MainTemplateView(TemplateView):
    template_name = "messenger/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing_count"] = Mailing.objects.count()
        context["active_mailing_count"] = Mailing.objects.filter(status="Запущена").count()
        context["unique_clients_count"] = Client.objects.count()
        return context


class StatisticsView(TemplateView):
    template_name = "messenger/statistics.html"

    def get_queryset(self):
        return Attempt.objects.filter(mailing__owner_id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["successful_attempts"] = queryset.filter(status="Успешно").count()
        context["unsuccessful_attempts"] = queryset.filter(status="Не успешно").count()
        context["total_mailings"] = queryset.count()
        return context


class StartMailingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "messenger.can_start_mailings"

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk")
        call_command("start_mailing", str(pk))
        return redirect("messenger:mailing_list")


class EndMailingView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    fields = []
    success_url = reverse_lazy("messenger:mailing_list")
    permission_required = "messenger.can_end_mailings"

    def form_valid(self, form):
        self.object.status = "Завершена"
        self.object.save()
        return super().form_valid(form)


class MailingStartTemplateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    fields = []
    success_url = reverse_lazy("messenger:mailing_list")
    template_name = "messenger/mailing_confirm_start.html"
    permission_required = "messenger.can_start_mailings"


class MailingEndTemplateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    fields = []
    success_url = reverse_lazy("messenger:mailing_list")
    template_name = "messenger/mailing_confirm_end.html"
    permission_required = "messenger.can_end_mailings"


class ClientDetailView(LoginRequiredMixin, ManagerMixin, DetailView):
    model = Client


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = "messenger.view_client"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ManagerMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("messenger:client_list")
    permission_required = "messenger.delete_client"


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = forms.ClientForm
    success_url = reverse_lazy("messenger:client_list")
    permission_required = "messenger.add_client"

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("messenger:client_detail", args=[self.object.pk])


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, ManagerMixin, UpdateView):
    model = Client
    fields = ["email", "name", "comment"]
    success_url = reverse_lazy("messenger:client_list")
    permission_required = "messenger.change_client"

    def get_success_url(self):
        return reverse_lazy("messenger:client_detail", args=[self.kwargs.get("pk")])


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, ManagerMixin, DetailView):
    model = Message
    permission_required = "messenger.view_message"


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    permission_required = "messenger.view_message"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ManagerMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("messenger:message_list")
    permission_required = "messenger.delete_message"


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = forms.MessageForm
    success_url = reverse_lazy("messenger:message_list")
    permission_required = "messenger.add_message"

    def get_success_url(self):
        return reverse_lazy("messenger:message_detail", args=[self.object.pk])


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, ManagerMixin, UpdateView):
    model = Message
    fields = ["topic", "content"]
    success_url = reverse_lazy("messenger:message_list")
    permission_required = "messenger.change_message"

    def get_success_url(self):
        return reverse_lazy("messenger:message_detail", args=[self.kwargs.get("pk")])


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, ManagerMixin, DetailView):
    model = Mailing
    permission_required = "messenger.view_mailing"


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = "messenger.view_mailing"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class ActiveMailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = "messenger.view_mailing"

    def get_queryset(self):
        queryset = super().get_queryset().filter(status="Запущена")
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ManagerMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("messenger:mailing_list")
    permission_required = "messenger.delete_mailing"


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = forms.MailingForm
    success_url = reverse_lazy("messenger:mailing_list")
    permission_required = "messenger.add_mailing"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("messenger:mailing_detail", args=[self.object.pk])


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, ManagerMixin, UpdateView):
    model = Mailing
    fields = ["sending_start", "sending_end", "message", "clients"]
    success_url = reverse_lazy("messenger:mailing_list")
    permission_required = "messenger.change_mailing"

    def get_success_url(self):
        return reverse_lazy("messenger:mailing_detail", args=[self.kwargs.get("pk")])


class UserClients(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = "messenger.view_client"

    def get_queryset(self):
        user = self.request.user
        return Client.objects.filter(owner=user)


class UserMailings(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = "messenger.view_mailing"

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(owner=user)
