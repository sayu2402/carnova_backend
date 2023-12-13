# Generated by Django 4.2.1 on 2023-12-11 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_useraccount_managers_alter_useraccount_groups_and_more'),
        ('vendor', '0004_carhandling_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='carhandling',
            name='verification_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='carhandling',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.vendorprofile'),
        ),
    ]