from django.urls import path

from messenger.apps import MessengerConfig

from . import views

app_name = MessengerConfig.name

urlpatterns = []
