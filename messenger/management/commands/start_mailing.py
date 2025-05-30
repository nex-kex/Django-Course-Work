from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from messenger.models import Mailing
import os


class Command(BaseCommand):
    help = "Start mailing"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")


    def handle(self, *args, **options):

        mailing_id = options["mailing_id"]
        mailing = Mailing.objects.get(pk=mailing_id)

        if timezone.now() > mailing.sending_end:
            mailing.status = "Завершена"
            mailing.save()

        else:
            mailing.status = "Запущена"
            mailing.save()

            send_mail(
                mailing.message.topic,
                mailing.message.content,
                os.getenv("EMAIL_HOST_USER"),
                [client.email for client in mailing.clients.all()],
                fail_silently=False,
            )