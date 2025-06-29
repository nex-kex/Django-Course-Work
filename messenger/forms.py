from django import forms
from .mixins import FormControlMixin
from . import models


class ClientForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = models.Client
        fields = ["email", "name", "comment"]


class MessageForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = models.Message
        fields = ["topic", "content"]


class MailingForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = models.Mailing
        fields = ["sending_start", "sending_end", "message", "clients"]
