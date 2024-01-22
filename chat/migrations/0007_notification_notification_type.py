# Generated by Django 5.0.1 on 2024-01-22 14:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0006_notification"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[("car_approved", "Car Approved")],
                default="pending",
                max_length=20,
            ),
        ),
    ]
