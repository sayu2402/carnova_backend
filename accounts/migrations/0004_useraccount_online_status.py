# Generated by Django 5.0.1 on 2024-01-15 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "accounts",
            "0003_alter_useraccount_managers_alter_useraccount_groups_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="online_status",
            field=models.BooleanField(default=False),
        ),
    ]
