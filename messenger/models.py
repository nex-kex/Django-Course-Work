from django.db import models


class Client(models.Model):
    email = models.CharField(max_length=150, unique=True, verbose_name="Email")
    name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["name", "email"]


class Message(models.Model):
    topic = models.CharField(max_length=100, verbose_name="Тема письма")
    content = models.TextField(verbose_name="Текст письма")

    def __str__(self):
        return f"{self.topic}"

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
    clients = models.ManyToManyField(
        Client, related_name="mailing", verbose_name="Получатели"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-status", "sending_start"]


class Attempt(models.Model):
    attempt_time = models.DateTimeField(verbose_name="Дата и время попытки")
    status = models.CharField(
        max_length=10,
        choices=[("Успешно", "Успешно"), ("Не успешно", "Не успешно")],
        verbose_name="Статус",
    )
    response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.SET_NULL,
        verbose_name="Сообщение",
        null=True,
        related_name="attempt",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["attempt_time"]
