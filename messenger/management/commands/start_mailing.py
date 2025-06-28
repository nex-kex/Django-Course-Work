import os

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from messenger.models import Attempt, Mailing


class Command(BaseCommand):
    help = "Start mailing"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **kwargs):

        mailing_id = kwargs["mailing_id"]
        mailing = Mailing.objects.get(pk=mailing_id)

        attempt = Attempt.objects.create(mailing=mailing)

        self._mailing_ended(mailing)

        if self._mailing_ended(mailing):

            mailing.status = "Завершена"
            mailing.save()

            attempt.status = "Не успешно"
            attempt.response = "Рассылка завершилась"
            attempt.save()

        else:
            self._send_emails(mailing, attempt)

    def _mailing_ended(self, mailing):
        """Проверка на случай, если рассылка завершилась"""

        return mailing.sending_end < timezone.now() or mailing.status == "Завершена"

    def _send_emails(self, mailing, attempt):
        """Отправка писем с обработкой SMTP ответа"""

        clients_emails = [client.email for client in mailing.clients.all()]

        try:
            if not clients_emails:
                raise ValueError("Не указаны получатели для рассылки")

            send_mail(
                subject=mailing.message.topic,
                message=mailing.message.content,
                from_email=os.getenv("EMAIL_HOST_USER"),
                recipient_list=clients_emails,
                fail_silently=False,
            )

            mailing.status = "Запущена"
            mailing.save()

            attempt.status = "Успешно"
            attempt.response = "Успешная попытка рассылки"
            attempt.save()

        except Exception as e:
            attempt.status = "Не успешно"
            attempt.response = f"{e}"
            attempt.save()
