# Generated by Django 5.0.1 on 2024-01-22 14:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0005_remove_chat_thread_name_chat_booking"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.CharField(max_length=100)),
            ],
        ),
    ]
