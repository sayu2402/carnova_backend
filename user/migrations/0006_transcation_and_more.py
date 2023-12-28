# Generated by Django 4.2.1 on 2023-12-27 11:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_useraccount_managers_alter_useraccount_groups_and_more'),
        ('user', '0005_remove_booking_pickup_date_must_be_greater_than_or_equal_to_today_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transcation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_share', models.DecimalField(decimal_places=2, max_digits=15)),
                ('company_share', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Payment ID')),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Order ID')),
                ('signature', models.CharField(blank=True, max_length=200, null=True, verbose_name='Signature')),
            ],
            options={
                'ordering': ['-transaction_date'],
            },
        ),
        migrations.RemoveConstraint(
            model_name='booking',
            name='pickup_date must be greater than or equal to today',
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.CheckConstraint(check=models.Q(('pickup_date__gte', datetime.datetime(2023, 12, 27, 11, 44, 2, 332689, tzinfo=datetime.timezone.utc))), name='pickup_date must be greater than or equal to today'),
        ),
        migrations.AddField(
            model_name='transcation',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.booking'),
        ),
        migrations.AddField(
            model_name='transcation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
        ),
        migrations.AddField(
            model_name='transcation',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.vendorprofile'),
        ),
    ]
