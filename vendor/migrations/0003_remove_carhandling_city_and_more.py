# Generated by Django 4.2.1 on 2023-12-11 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carhandling',
            name='city',
        ),
        migrations.RemoveField(
            model_name='carhandling',
            name='property_address',
        ),
        migrations.RemoveField(
            model_name='carhandling',
            name='state',
        ),
        migrations.RemoveField(
            model_name='carhandling',
            name='zip_code',
        ),
    ]