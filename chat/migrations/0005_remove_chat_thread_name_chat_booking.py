# Generated by Django 5.0.1 on 2024-01-13 14:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0004_chat_thread_name"),
        ("user", "0002_wallet"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chat",
            name="thread_name",
        ),
        migrations.AddField(
            model_name="chat",
            name="booking",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="user.booking",
            ),
        ),
    ]
