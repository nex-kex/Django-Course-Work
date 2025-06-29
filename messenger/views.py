from django.core.management import call_command
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)

from . import forms
from .models import Client, Mailing, Message


class MainTemplateView(TemplateView):
    template_name = "messenger/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing_count"] = Mailing.objects.count()
        context["active_mailing_count"] = Mailing.objects.filter(
            status="Запущена"
        ).count()
        context["unique_clients_count"] = Client.objects.count()
        return context


class StartMailingView(View):

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk")
        call_command("start_mailing", str(pk))
        return redirect("messenger:mailing_list")


class EndMailingView(UpdateView):
    model = Mailing
    fields = []
    success_url = reverse_lazy("messenger:mailing_list")

    def form_valid(self, form):
        self.object.status = "Завершена"
        self.object.save()
        return super().form_valid(form)


class MailingStartTemplateView(UpdateView):
    model = Mailing
    fields = []
    success_url = reverse_lazy("messenger:mailing_list")
    template_name = "messenger/mailing_confirm_start.html"


class MailingEndTemplateView(UpdateView):
    model = Mailing
    fields = []
    success_url = reverse_lazy("messenger:mailing_list")
    template_name = "messenger/mailing_confirm_end.html"


class ClientDetailView(DetailView):
    model = Client


class ClientListView(ListView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("messenger:client_list")


class ClientCreateView(CreateView):
    model = Client
    form_class = forms.ClientForm
    success_url = reverse_lazy("messenger:client_list")

    def get_success_url(self):
        return reverse_lazy("messenger:client_detail", args=[self.object.pk])


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["email", "name", "comment"]
    success_url = reverse_lazy("messenger:client_list")

    def get_success_url(self):
        return reverse_lazy("messenger:client_detail", args=[self.kwargs.get("pk")])


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("messenger:message_list")


class MessageCreateView(CreateView):
    model = Message
    form_class = forms.MessageForm
    success_url = reverse_lazy("messenger:message_list")

    def get_success_url(self):
        return reverse_lazy("messenger:message_detail", args=[self.object.pk])


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["topic", "content"]
    success_url = reverse_lazy("messenger:message_list")

    def get_success_url(self):
        return reverse_lazy("messenger:message_detail", args=[self.kwargs.get("pk")])


class MailingDetailView(DetailView):
    model = Mailing


class MailingListView(ListView):
    model = Mailing


class ActiveMailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status="Запущена")


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy("messenger:mailing_list")


class MailingCreateView(CreateView):
    model = Mailing
    form_class = forms.MailingForm
    success_url = reverse_lazy("messenger:mailing_list")

    def get_success_url(self):
        return reverse_lazy("messenger:mailing_detail", args=[self.object.pk])


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ["sending_start", "sending_end", "message", "clients"]
    success_url = reverse_lazy("messenger:mailing_list")

    def get_success_url(self):
        return reverse_lazy("messenger:mailing_detail", args=[self.kwargs.get("pk")])
