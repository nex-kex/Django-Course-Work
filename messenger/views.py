from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from .models import Client, Message, Mailing


class ClientDetailView(DetailView):
    model = Client


class ClientListView(ListView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('messenger:clients_list')


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'name', 'comment']
    success_url = reverse_lazy('messenger:clients_list')

    def get_success_url(self):
        return reverse_lazy("messenger:client_detail", args=[self.object.pk])


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'name', 'comment']
    success_url = reverse_lazy('messenger:clients_list')

    def get_success_url(self):
        return reverse_lazy("messenger:client_detail", args=[self.kwargs.get("pk")])


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('messenger:messages_list')


class MessageCreateView(CreateView):
    model = Message
    fields = ['topic', 'content']
    success_url = reverse_lazy('messenger:messages_list')

    def get_success_url(self):
        return reverse_lazy("messenger:message_detail", args=[self.object.pk])


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['topic', 'content']
    success_url = reverse_lazy('messenger:messages_list')

    def get_success_url(self):
        return reverse_lazy("messenger:message_detail", args=[self.kwargs.get("pk")])


class MailingDetailView(DetailView):
    model = Mailing


class MailingListView(ListView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('messenger:mailings_list')


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['sending_start', 'sending_end', 'status', 'message', 'clients']
    success_url = reverse_lazy('messenger:mailings_list')

    def get_success_url(self):
        return reverse_lazy("messenger:mailing_detail", args=[self.object.pk])


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['sending_start', 'sending_end', 'status', 'message', 'clients']
    success_url = reverse_lazy('messenger:mailings_list')

    def get_success_url(self):
        return reverse_lazy("messenger:mailing_detail", args=[self.kwargs.get("pk")])
