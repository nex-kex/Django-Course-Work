from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView

from .models import Client, Message, Mailing


class MainTemplateView(TemplateView):

    template_name = 'messenger/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = Mailing.objects.count()
        context['active_mailing_count'] = Mailing.objects.filter(status='Запущена').count()
        context['unique_clients_count'] = Client.objects.count()
        return context


class ClientDetailView(DetailView):
    model = Client


class ClientListView(ListView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('messenger:client_list')


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'name', 'comment']
    success_url = reverse_lazy('messenger:client_list')

    def get_success_url(self):
        return reverse_lazy("messenger:client_detail", args=[self.object.pk])


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'name', 'comment']
    success_url = reverse_lazy('messenger:client_list')

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
    success_url = reverse_lazy('messenger:message_list')

    def get_success_url(self):
        return reverse_lazy("messenger:message_detail", args=[self.object.pk])


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['topic', 'content']
    success_url = reverse_lazy('messenger:message_list')

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
    success_url = reverse_lazy('messenger:mailing_list')


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['sending_start', 'sending_end', 'status', 'message', 'clients']
    success_url = reverse_lazy('messenger:mailing_list')

    def get_success_url(self):
        return reverse_lazy("messenger:mailing_detail", args=[self.object.pk])


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['sending_start', 'sending_end', 'status', 'message', 'clients']
    success_url = reverse_lazy('messenger:mailing_list')

    def get_success_url(self):
        return reverse_lazy("messenger:mailing_detail", args=[self.kwargs.get("pk")])
