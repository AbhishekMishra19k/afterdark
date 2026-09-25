from django.conf import settings
from django.core.mail import send_mail


def send_booking_confirmation(booking):
    """Send a confirmation email after a booking is created.
    Uses the console backend by default (prints to terminal) until
    EMAIL_BACKEND/EMAIL_HOST_* env vars are set for real SMTP delivery.
    """
    subject = "AFTERDARK — Your booking is received"
    message = (
        f"Hi {booking.full_name},\n\n"
        f"Thanks for booking AFTERDARK! Here are your details:\n\n"
        f"Entry type: {booking.get_entry_type_display()}\n"
        f"Amount due: Rs. {booking.price}\n"
        f"Booking ID: {booking.id}\n"
        f"Payment status: {booking.get_payment_status_display()}\n\n"
        f"If you haven't completed payment yet, please pay using the QR code / "
        f"bank details on the booking page and submit your payment reference so "
        f"we can confirm your spot.\n\n"
        f"Reminder: Entry is strictly 18+. Please carry a valid original "
        f"government photo ID — entry will be refused without it.\n\n"
        f"See you on the dance floor.\n"
        f"— Team AFTERDARK, Indore"
    )
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.email],
            fail_silently=True,
        )
        booking.confirmation_email_sent = True
        booking.save(update_fields=["confirmation_email_sent"])
    except Exception:
        # Never let email failure break the booking flow.
        pass
