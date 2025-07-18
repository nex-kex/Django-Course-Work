from django.db import models

import users.models


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        users.models.CustomUser,
        on_delete=models.CASCADE,
        related_name="client_owners",
        verbose_name="Создатель",
        null=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["name", "email"]


class Message(models.Model):
    topic = models.CharField(max_length=100, verbose_name="Тема письма")
    content = models.TextField(verbose_name="Текст письма")
    owner = models.ForeignKey(
        users.models.CustomUser,
        on_delete=models.CASCADE,
        related_name="message_owners",
        verbose_name="Создатель",
        null=True,
    )

    def __str__(self):
        return f'[ID: {self.pk}] "{self.topic}"'

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"


class Mailing(models.Model):
    sending_start = models.DateTimeField(verbose_name="Дата и время первой отправки")
    sending_end = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=9,
        default="Создана",
        choices=[
            ("Завершена", "Завершена"),
            ("Создана", "Создана"),
            ("Запущена", "Запущена"),
        ],
        verbose_name="Статус",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailing",
        verbose_name="Сообщение",
    )
    clients = models.ManyToManyField(Client, related_name="mailing", verbose_name="Получатели")
    owner = models.ForeignKey(
        users.models.CustomUser, on_delete=models.CASCADE, related_name="mailings", verbose_name="Создатель", null=True
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-status", "sending_start"]
        permissions = [
            ("can_start_mailings", "Can start mailings"),
            ("can_end_mailings", "Can end mailings"),
        ]


class Attempt(models.Model):
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(
        max_length=10,
        choices=[("Успешно", "Успешно"), ("Не успешно", "Не успешно")],
        verbose_name="Статус",
    )
    response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="attempt",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-attempt_time"]
