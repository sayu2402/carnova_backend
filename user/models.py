from django.db import models
from django.utils import timezone
from vendor.models import CarHandling, VendorProfile
from accounts.models import UserProfile
import datetime
import uuid


class Booking(models.Model):
    car = models.ForeignKey(CarHandling, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, default=None)
    pickup_date = models.DateField()
    return_date = models.DateField()
    total_amount = models.PositiveIntegerField()
    is_cancelled = models.BooleanField(default=False)
    order_number = models.CharField(
        max_length=50, unique=True, default="", editable=False
    )

    VERIFICATION_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_STATUS_CHOICES,
        default="pending",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(return_date__gt=models.F("pickup_date")),
                name="return_date must be greater than pickup_date",
            )
        ]

    def save(self, *args, **kwargs):
        # Generate order number if not provided
        if not self.order_number:
            self.order_number = generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking ID: {self.id}"


class Transcation(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    vendor_share = models.DecimalField(max_digits=15, decimal_places=2)
    company_share = models.DecimalField(max_digits=15, decimal_places=2)

    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(
        max_length=100, verbose_name="Payment ID", null=True, blank=True
    )
    order_id = models.CharField(
        max_length=100, verbose_name="Order ID", null=True, blank=True
    )
    signature = models.CharField(
        max_length=200, verbose_name="Signature", null=True, blank=True
    )

    def __str__(self):
        return str(self.id)


def generate_order_number():
    yr = int(datetime.date.today().strftime("%Y"))
    dt = int(datetime.date.today().strftime("%d"))
    mt = int(datetime.date.today().strftime("%m"))
    d = datetime.date(yr, mt, dt)
    current_date = d.strftime("%Y%m%d")
    unique_id = str(uuid.uuid4().hex)[:8]
    return current_date + unique_id


class Wallet(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


class IDCard(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    front_photo = models.ImageField(upload_to="", null=True, blank=True)
    back_photo = models.ImageField(upload_to="", null=True, blank=True)

    def __str__(self):
        return f"IDCard - {self.user_profile.user.username}"
