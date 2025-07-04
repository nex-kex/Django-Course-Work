# Generated by Django 5.2.1 on 2025-05-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("messenger", "0003_alter_client_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="status",
            field=models.CharField(
                choices=[
                    ("Завершена", "Завершена"),
                    ("Создана", "Создана"),
                    ("Запущена", "Запущена"),
                ],
                default="Создана",
                max_length=9,
                verbose_name="Статус",
            ),
        ),
    ]
