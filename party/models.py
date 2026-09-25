from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class SiteConfig(models.Model):
    """Singleton-style config the admin edits from Django admin."""

    event_datetime = models.DateTimeField(
        help_text="Drives the homepage countdown timer."
    )
    single_price = models.PositiveIntegerField(default=499)
    couple_price = models.PositiveIntegerField(default=899)

    payment_qr_image = models.ImageField(
        upload_to="payment/", blank=True, null=True,
        help_text="Upload a UPI/QR code image (optional)."
    )
    bank_details = models.TextField(
        blank=True,
        help_text="Account name, number, IFSC, UPI ID, etc. (optional)."
    )
    razorpay_enabled = models.BooleanField(default=False)
    razorpay_key_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_link = models.URLField(
        blank=True, help_text="Optional Razorpay Payment Link / Payment Page URL."
    )

    venue_name = models.CharField(max_length=200, default="AFTERDARK, Indore")
    address = models.CharField(max_length=300, default="Indore, Madhya Pradesh")
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    instagram_url = models.URLField(blank=True)
    terms_and_conditions = models.TextField(
        default="Entry strictly 18+. Valid government photo ID proof is mandatory at entry. "
                "Management reserves the right of admission. No refunds on cancelled bookings "
                "unless the event itself is cancelled."
    )

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "AFTERDARK Site Configuration"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            "event_datetime": timezone.now()
        })
        return obj


class UpcomingEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="upcoming/", blank=True, null=True)
    is_active = models.BooleanField(
        default=True, help_text="Only active event shows on homepage."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-event_date"]

    def __str__(self):
        return f"{self.title} — {self.event_date:%d %b %Y}"


class PastEventPhoto(models.Model):
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=150, blank=True)
    event_name = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-uploaded_at"]

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    guest_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    review_text = models.TextField()
    event_name = models.CharField(max_length=150, blank=True)
    is_approved = models.BooleanField(
        default=True, help_text="Uncheck to hide a review from the homepage."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.guest_name} ({self.rating}★)"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Booking(models.Model):
    ENTRY_SINGLE = "single"
    ENTRY_COUPLE = "couple"
    ENTRY_CHOICES = [
        (ENTRY_SINGLE, "Single Entry"),
        (ENTRY_COUPLE, "Couple Entry"),
    ]

    PAYMENT_PENDING = "pending"
    PAYMENT_SUBMITTED = "submitted"
    PAYMENT_CONFIRMED = "confirmed"
    PAYMENT_REJECTED = "rejected"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, "Pending"),
        (PAYMENT_SUBMITTED, "Reference Submitted"),
        (PAYMENT_CONFIRMED, "Confirmed"),
        (PAYMENT_REJECTED, "Rejected"),
    ]

    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=150)
    screening_answer = models.TextField(
        verbose_name="Why do you want to attend?"
    )
    entry_type = models.CharField(max_length=10, choices=ENTRY_CHOICES)
    price = models.PositiveIntegerField(help_text="Price locked in at booking time.")

    payment_reference = models.CharField(
        max_length=150, blank=True,
        help_text="UPI transaction ID / UTR / Razorpay payment ID"
    )
    payment_status = models.CharField(
        max_length=12, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING
    )

    confirmation_email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.get_entry_type_display()} ({self.payment_status})"
