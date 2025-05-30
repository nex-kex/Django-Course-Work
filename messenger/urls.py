from django.urls import path

from messenger.apps import MessengerConfig

from . import views

app_name = MessengerConfig.name

urlpatterns = [
    path("", views.MainTemplateView.as_view(), name="main"),

    path(
        "mailing/<int:pk>/start/",
        views.StartMailingView.as_view(),
        name="mailing_start",
    ),

    path(
        "mailing/<int:pk>/end/",
        views.EndMailingView.as_view(),
        name="mailing_end",
    ),

    path("mailing/<int:pk>/start/confirm/", views.MailingStartTemplateView.as_view(), name="mailing_start_confirm"),
    path("mailing/<int:pk>/end/confirm/", views.MailingEndTemplateView.as_view(), name="mailing_end_confirm"),

    path("client/create/", views.ClientCreateView.as_view(), name="client_create"),
    path("message/create/", views.MessageCreateView.as_view(), name="message_create"),
    path("mailing/create/", views.MailingCreateView.as_view(), name="mailing_create"),

    path("client/list/", views.ClientListView.as_view(), name="client_list"),
    path("message/list/", views.MessageListView.as_view(), name="message_list"),
    path("mailing/list/", views.MailingListView.as_view(), name="mailing_list"),
    path(
        "mailing/list/active/",
        views.ActiveMailingListView.as_view(),
        name="mailing_list_active",
    ),

    path("client/<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),
    path("message/<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"),
    path("mailing/<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),

    path(
        "client/<int:pk>/delete/",
        views.ClientDeleteView.as_view(),
        name="client_delete",
    ),
    path(
        "message/<int:pk>/delete/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path(
        "mailing/<int:pk>/delete/",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),

    path(
        "client/<int:pk>/update/",
        views.ClientUpdateView.as_view(),
        name="client_update",
    ),
    path(
        "message/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "mailing/<int:pk>/update/",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
]
