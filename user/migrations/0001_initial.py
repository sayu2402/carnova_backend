# Generated by Django 4.2.1 on 2024-01-03 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        (
            "accounts",
            "0003_alter_useraccount_managers_alter_useraccount_groups_and_more",
        ),
        ("vendor", "0005_carhandling_verification_status_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
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
                ("pickup_date", models.DateField()),
                ("return_date", models.DateField()),
                ("total_amount", models.PositiveIntegerField()),
                ("is_cancelled", models.BooleanField(default=False)),
                (
                    "order_number",
                    models.CharField(
                        default="", editable=False, max_length=50, unique=True
                    ),
                ),
                (
                    "verification_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vendor.carhandling",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.userprofile",
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.vendorprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transcation",
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
                ("vendor_share", models.DecimalField(decimal_places=2, max_digits=15)),
                ("company_share", models.DecimalField(decimal_places=2, max_digits=15)),
                ("transaction_date", models.DateTimeField(auto_now_add=True)),
                (
                    "payment_id",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Payment ID"
                    ),
                ),
                (
                    "order_id",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Order ID"
                    ),
                ),
                (
                    "signature",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Signature"
                    ),
                ),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.booking"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.userprofile",
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.vendorprofile",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.CheckConstraint(
                check=models.Q(("return_date__gt", models.F("pickup_date"))),
                name="return_date must be greater than pickup_date",
            ),
        ),
    ]
