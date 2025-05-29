from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from .models import Client, Message, Mailing, Attempt


class ClientCreateView(CreateView):
    pass


class ClientDetailView(DetailView):
    pass


class ClientListView(ListView):
    pass


class ClientUpdateView(UpdateView):
    pass


class ClientDeleteView(DeleteView):
    pass


class MessageCreateView(CreateView):
    pass


class MessageDetailView(DetailView):
    pass


class MessageListView(ListView):
    pass


class MessageUpdateView(UpdateView):
    pass


class MessageDeleteView(DeleteView):
    pass


class MailingCreateView(CreateView):
    pass


class MailingDetailView(DetailView):
    pass


class MailingListView(ListView):
    pass


class MailingUpdateView(UpdateView):
    pass


class MailingDeleteView(DeleteView):
    pass
