from django.urls import path

from messenger.apps import MessengerConfig

from . import views

app_name = MessengerConfig.name

urlpatterns = [
    path("", views.MainTemplateView.as_view(), name="main"),

    path("client/create/", views.ClientCreateView.as_view(), name="client_create"),
    path("message/create/", views.MessageCreateView.as_view(), name="message_create"),
    path("mailing/create/", views.MailingCreateView.as_view(), name="mailing_create"),

    path("client/list/", views.ClientListView.as_view(), name="client_list"),
    path("message/list/", views.MessageListView.as_view(), name="message_list"),
    path("mailing/list/", views.MailingListView.as_view(), name="mailing_list"),
]
