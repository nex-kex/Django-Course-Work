from django.urls import path

from messenger.apps import MessengerConfig

from . import views

app_name = MessengerConfig.name

urlpatterns = [
    path("", views.MainTemplateView.as_view(), name="main"),

    path("client/create/", views.ClientCreateView.as_view(), name="client_create"),
    path("message/create/", views.MessageCreateView.as_view(), name="message_create"),
    path("mailing/create/", views.MailingCreateView.as_view(), name="mailing_create"),


]
