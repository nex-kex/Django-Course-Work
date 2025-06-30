from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    reset_password_token = models.CharField(max_length=100, verbose_name="Reset password token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
        permissions = [
            ("can_block_users", "Can block users"),
        ]

    def __str__(self):
        return self.email
