# Generated by Django 4.2.1 on 2023-12-27 07:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_booking_pickup_date_must_be_greater_than_or_equal_to_today_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='booking',
            name='pickup_date must be greater than or equal to today',
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.CheckConstraint(check=models.Q(('pickup_date__gte', datetime.datetime(2023, 12, 27, 7, 29, 58, 327385, tzinfo=datetime.timezone.utc))), name='pickup_date must be greater than or equal to today'),
        ),
    ]
