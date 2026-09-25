import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import (
    SiteConfig, UpcomingEvent, PastEventPhoto, Review,
    ContactMessage, Booking,
)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Countdown", {"fields": ("event_datetime",)}),
        ("Pricing", {"fields": ("single_price", "couple_price")}),
        ("Payment method (shown to guests at checkout)", {
            "fields": ("payment_qr_image", "bank_details",
                       "razorpay_enabled", "razorpay_key_id", "razorpay_payment_link"),
        }),
        ("Venue & contact", {
            "fields": ("venue_name", "address", "contact_phone",
                       "contact_email", "instagram_url"),
        }),
        ("Legal", {"fields": ("terms_and_conditions",)}),
    )

    def has_add_permission(self, request):
        # Singleton: only one config row.
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)


@admin.register(PastEventPhoto)
class PastEventPhotoAdmin(admin.ModelAdmin):
    list_display = ("caption", "event_name", "order", "is_visible", "uploaded_at")
    list_editable = ("order", "is_visible")
    list_filter = ("is_visible",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("guest_name", "rating", "event_name", "is_approved", "created_at")
    list_editable = ("is_approved",)
    list_filter = ("is_approved", "rating")
    search_fields = ("guest_name", "review_text")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "is_read")
    list_editable = ("is_read",)
    readonly_fields = ("name", "email", "phone", "message", "created_at")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "age", "email", "location", "entry_type",
        "price", "payment_status", "created_at",
    )
    list_editable = ("payment_status",)
    list_filter = ("entry_type", "payment_status", "created_at")
    search_fields = ("full_name", "email", "location", "payment_reference")
    readonly_fields = ("created_at", "confirmation_email_sent")
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="afterdark_bookings.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Full Name", "Age", "Email", "Phone", "Location", "Entry Type",
            "Price", "Payment Status", "Payment Reference", "Screening Answer",
            "Booked At",
        ])
        for b in queryset:
            writer.writerow([
                b.full_name, b.age, b.email, b.phone, b.location,
                b.get_entry_type_display(), b.price, b.get_payment_status_display(),
                b.payment_reference, b.screening_answer, b.created_at,
            ])
        return response

    export_as_csv.short_description = "Export selected bookings to CSV"
