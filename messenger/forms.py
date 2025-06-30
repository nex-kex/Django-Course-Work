from django import forms

from . import models
from .mixins import FormControlMixin
from .models import Client, Message


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.groups.filter(name='Менеджеры').exists():
                self.fields['clients'].queryset = Client.objects.all()
                self.fields['message'].queryset = Message.objects.all()
            else:
                self.fields['clients'].queryset = Client.objects.filter(owner=user)
                self.fields['message'].queryset = Message.objects.filter(owner=user)
